from odoo import models, fields
from odoo.exceptions import UserError


class EmployeeLoanPaymentWizard(models.TransientModel):
    _name = 'employee.loan.payment.wizard'
    _description = 'Employee Loan Payment Wizard'

    loan_id = fields.Many2one('employee.loan', required=True)
    company_id = fields.Many2one(related='loan_id.company_id', readonly=True)
    currency_id = fields.Many2one(related='company_id.currency_id', readonly=True)
    transaction_type = fields.Selection([
        ('debit', 'Prestamo'),
        ('credit', 'Abono'),
    ], string='Tipo de movimiento', required=True, default='credit')
    date = fields.Date(string='Fecha', default=fields.Date.context_today, required=True)
    journal_id = fields.Many2one(
        'account.journal',
        string='Diario caja/banco',
        domain="[('type', 'in', ('cash', 'bank')), ('company_id', '=', company_id)]",
        required=True,
    )
    amount = fields.Monetary(string='Monto', currency_field='currency_id', required=True)
    ref = fields.Char(string='Referencia')

    def action_apply(self):
        self.ensure_one()

        if self.amount <= 0:
            raise UserError('El monto debe ser mayor a 0')

        if not self.loan_id._get_effective_loan_account():
            raise UserError('Configura la cuenta de prestamos en la ficha del empleado')

        self.env['employee.loan.line'].create({
            'loan_id': self.loan_id.id,
            'date': self.date,
            'amount': self.amount,
            'type': self.transaction_type,
            'origin': 'manual',
            'journal_id': self.journal_id.id,
        })

        return {'type': 'ir.actions.act_window_close'}
