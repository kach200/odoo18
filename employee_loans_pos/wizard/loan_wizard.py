
from odoo import models, fields
from odoo.exceptions import UserError

class EmployeeLoanWizard(models.TransientModel):
    _name = 'employee.loan.wizard'

    loan_id = fields.Many2one('employee.loan', required=True)
    amount = fields.Float(required=True)

    def action_apply(self):
        self.ensure_one()
        loan = self.loan_id
        general_journal = loan._get_effective_general_journal()
        loan_account = loan._get_effective_loan_account()
        counterpart_account = loan._get_effective_counterpart_account()

        if self.amount <= 0:
            raise UserError("El saldo inicial debe ser mayor a 0")

        if loan.line_ids.filtered(lambda l: l.type == 'initial'):
            raise UserError("Ya existe saldo inicial")

        if not general_journal or not loan_account or not counterpart_account:
            raise UserError("Configura diario contable, cuenta de prestamos y cuenta contrapartida en la ficha del empleado")

        move = self.env['account.move'].create({
            'move_type': 'entry',
            'date': fields.Date.context_today(self),
            'journal_id': general_journal.id,
            'ref': 'Saldo inicial prestamo - %s' % loan.employee_id.name,
            'line_ids': [
                (0, 0, {
                    'name': 'Saldo inicial prestamo - %s' % loan.employee_id.name,
                    'account_id': loan_account.id,
                    'debit': self.amount,
                    'credit': 0.0,
                }),
                (0, 0, {
                    'name': 'Saldo inicial prestamo - %s' % loan.employee_id.name,
                    'account_id': counterpart_account.id,
                    'debit': 0.0,
                    'credit': self.amount,
                }),
            ],
        })
        move.action_post()

        self.env['employee.loan.line'].create({
            'loan_id': loan.id,
            'amount': self.amount,
            'type': 'initial',
            'origin': 'manual',
            'account_move_id': move.id,
        })
