
from odoo import models, fields, api
from odoo.exceptions import UserError

class EmployeeLoan(models.Model):
    _name = 'employee.loan'
    _description = 'Employee Loan'

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, required=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Empleado', required=True)
    line_ids = fields.One2many('employee.loan.line', 'loan_id')
    balance = fields.Float(string='Saldo de deuda', compute='_compute_balance', store=True)
    has_initial_balance = fields.Boolean(compute='_compute_has_initial_balance')

    @api.depends('line_ids.amount', 'line_ids.type')
    def _compute_balance(self):
        for rec in self:
            debit = sum(l.amount for l in rec.line_ids if l.type in ['debit','initial'])
            credit = sum(l.amount for l in rec.line_ids if l.type == 'credit')
            rec.balance = debit - credit

    @api.depends('line_ids.type')
    def _compute_has_initial_balance(self):
        for rec in self:
            rec.has_initial_balance = any(line.type == 'initial' for line in rec.line_ids)

    def load_initial_balance(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Saldo Inicial',
            'res_model': 'employee.loan.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_loan_id': self.id}
        }

    def _get_effective_general_journal(self):
        self.ensure_one()
        return self.employee_id.loan_journal_id

    def _get_effective_loan_account(self):
        self.ensure_one()
        return self.employee_id.loan_account_id

    def _get_effective_counterpart_account(self):
        self.ensure_one()
        return self.employee_id.loan_counterpart_account_id

    def _get_effective_default_journal(self):
        self.ensure_one()
        return self.employee_id.loan_default_journal_id

    def action_open_transaction_wizard(self):
        self.ensure_one()
        tx_type = self.env.context.get('default_transaction_type', 'credit')
        action_name = 'Registrar Abono' if tx_type == 'credit' else 'Registrar Prestamo'
        default_journal = self._get_effective_default_journal()
        return {
            'type': 'ir.actions.act_window',
            'name': action_name,
            'res_model': 'employee.loan.payment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_loan_id': self.id,
                'default_transaction_type': tx_type,
                'default_journal_id': default_journal.id,
            },
        }

class EmployeeLoanLine(models.Model):
    _name = 'employee.loan.line'
    _description = 'Loan Movements'
    _order = 'date desc, id desc'

    loan_id = fields.Many2one('employee.loan', required=True)
    company_id = fields.Many2one(related='loan_id.company_id', store=True, readonly=True)
    account_move_id = fields.Many2one('account.move', string='Asiento contable', readonly=True)
    journal_id = fields.Many2one(
        'account.journal',
        string='Diario caja/banco',
        domain="[('type', 'in', ('cash', 'bank')), ('company_id', '=', company_id)]",
    )
    date = fields.Date(default=fields.Date.today)
    amount = fields.Float(required=True)
    type = fields.Selection([
        ('debit','Prestamo'),
        ('credit','Abono'),
        ('initial','Saldo Inicial')
    ], required=True)
    origin = fields.Selection([
        ('manual','Manual'),
        ('pos','POS')
    ], default='manual')
    loan_amount = fields.Float(string='Prestamo', compute='_compute_display_columns')
    payment_amount = fields.Float(string='Abono', compute='_compute_display_columns')
    running_balance = fields.Float(string='Saldo', compute='_compute_display_columns')

    @api.depends('loan_id.line_ids.amount', 'loan_id.line_ids.type', 'loan_id.line_ids.date')
    def _compute_display_columns(self):
        loans = self.mapped('loan_id')
        line_map = {}
        for loan in loans:
            running = 0.0
            ordered_lines = loan.line_ids.sorted(key=lambda l: ((l.date or fields.Date.today()), l.id))
            for line in ordered_lines:
                if line.type in ('debit', 'initial'):
                    running += line.amount
                    line_map[line.id] = (line.amount, 0.0, running)
                elif line.type == 'credit':
                    running -= line.amount
                    line_map[line.id] = (0.0, line.amount, running)
                else:
                    line_map[line.id] = (0.0, 0.0, running)

        for line in self:
            values = line_map.get(line.id, (0.0, 0.0, 0.0))
            line.loan_amount = values[0]
            line.payment_amount = values[1]
            line.running_balance = values[2]

    @api.onchange('type', 'loan_id')
    def _onchange_set_default_journal(self):
        for line in self:
            if line.type in ('debit', 'credit') and not line.journal_id:
                line.journal_id = line.loan_id._get_effective_default_journal()

    @api.constrains('amount', 'type', 'journal_id', 'loan_id')
    def _check_accounting_data(self):
        for line in self:
            if line.amount <= 0:
                raise UserError('El monto debe ser mayor a 0')

            if line.type in ('debit', 'credit') and not line.journal_id:
                raise UserError('Debes seleccionar un diario de caja/banco para prestamos y abonos')

            if line.type in ('debit', 'credit') and not line.loan_id._get_effective_loan_account():
                raise UserError('Configura la cuenta de prestamos en la ficha del empleado antes de registrar movimientos')

    def _get_liquidity_account(self):
        self.ensure_one()
        liquidity_account = self.journal_id.default_account_id
        if not liquidity_account:
            raise UserError('El diario seleccionado no tiene cuenta por defecto configurada')
        return liquidity_account

    def _prepare_move_vals(self):
        self.ensure_one()
        liquidity_account = self._get_liquidity_account()
        loan_account = self.loan_id._get_effective_loan_account()
        if not loan_account:
            raise UserError('Configura la cuenta de prestamos en la ficha del empleado')
        line_date = self.date or fields.Date.context_today(self)

        emp_name = self.loan_id.employee_id.name
        if self.type == 'debit':
            # Prestamo entregado: aumenta la cuenta por cobrar al empleado y sale dinero de caja/banco.
            debit_line = {
                'name': 'Prestamo a empleado - %s' % emp_name,
                'account_id': loan_account.id,
                'debit': self.amount,
                'credit': 0.0,
            }
            credit_line = {
                'name': 'Prestamo a empleado - %s' % emp_name,
                'account_id': liquidity_account.id,
                'debit': 0.0,
                'credit': self.amount,
            }
            ref = 'Prestamo empleado - %s' % emp_name
        elif self.type == 'credit':
            # Abono recibido: entra dinero en caja/banco y disminuye la cuenta por cobrar al empleado.
            debit_line = {
                'name': 'Abono de prestamo - %s' % emp_name,
                'account_id': liquidity_account.id,
                'debit': self.amount,
                'credit': 0.0,
            }
            credit_line = {
                'name': 'Abono de prestamo - %s' % emp_name,
                'account_id': loan_account.id,
                'debit': 0.0,
                'credit': self.amount,
            }
            ref = 'Abono prestamo - %s' % emp_name
        else:
            return False

        return {
            'move_type': 'entry',
            'date': line_date,
            'journal_id': self.journal_id.id,
            'ref': ref,
            'line_ids': [(0, 0, debit_line), (0, 0, credit_line)],
        }

    def _create_account_move_for_line(self):
        self.ensure_one()
        if self.account_move_id or self.type not in ('debit', 'credit'):
            return

        move_vals = self._prepare_move_vals()
        if not move_vals:
            return

        move = self.env['account.move'].create(move_vals)
        move.action_post()
        self.with_context(allow_loan_line_system_write=True).write({'account_move_id': move.id})

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            line_type = vals.get('type')
            if line_type in ('debit', 'credit') and not vals.get('journal_id') and vals.get('loan_id'):
                loan = self.env['employee.loan'].browse(vals['loan_id'])
                default_journal = loan._get_effective_default_journal()
                if default_journal:
                    vals['journal_id'] = default_journal.id

        lines = super().create(vals_list)
        for line in lines:
            line._create_account_move_for_line()
        return lines

    def write(self, vals):
        if not self.env.context.get('allow_loan_line_system_write'):
            raise UserError('Los movimientos son historicos y no se pueden editar. Usa el wizard para nuevos registros.')

        for line in self:
            if line.account_move_id and any(field in vals for field in ('amount', 'type', 'journal_id', 'loan_id', 'date')):
                raise UserError('No puedes modificar tipo, monto, fecha o diario en un movimiento ya contabilizado')

        res = super().write(vals)
        for line in self:
            line._create_account_move_for_line()
        return res

    def unlink(self):
        if not self.env.context.get('allow_loan_line_system_write'):
            raise UserError('Los movimientos son historicos y no se pueden eliminar.')
        return super().unlink()
