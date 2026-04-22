from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    loan_journal_id = fields.Many2one(
        'account.journal',
        string='Diario contable (prestamos)',
        groups='hr.group_hr_user',
        domain="[('type', '=', 'general')]",
    )
    loan_account_id = fields.Many2one(
        'account.account',
        string='Cuenta de prestamos',
        groups='hr.group_hr_user',
        domain="[('deprecated', '=', False)]",
    )
    loan_counterpart_account_id = fields.Many2one(
        'account.account',
        string='Cuenta contrapartida',
        groups='hr.group_hr_user',
        domain="[('deprecated', '=', False)]",
    )
    loan_default_journal_id = fields.Many2one(
        'account.journal',
        string='Diario por defecto (caja/banco)',
        groups='hr.group_hr_user',
        domain="[('type', 'in', ('cash', 'bank'))]",
    )
