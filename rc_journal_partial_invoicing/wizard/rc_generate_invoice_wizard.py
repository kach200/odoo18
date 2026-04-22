from odoo import fields, models, _
from odoo.exceptions import UserError


class RcGenerateInvoiceWizard(models.TransientModel):
    _name = "rc.generate.invoice.wizard"
    _description = "Generador de factura desde lote"

    batch_id = fields.Many2one("rc.invoice.batch", string="Lote", required=True)
    partner_id = fields.Many2one("res.partner", string="Cliente", required=True)
    journal_id = fields.Many2one(
        "account.journal", string="Diario", required=True, domain=[("type", "=", "sale")]
    )
    invoice_date = fields.Date(string="Fecha factura", default=fields.Date.context_today, required=True)

    def action_generate_invoice(self):
        self.ensure_one()
        batch = self.batch_id
        lines_to_invoice = batch.line_ids.filtered(lambda l: l.quantity_to_invoice > 0)
        if not lines_to_invoice:
            raise UserError(_("No hay cantidades a facturar."))

        invoice_line_commands = []
        for line in lines_to_invoice:
            invoice_line_commands.append(
                (
                    0,
                    0,
                    {
                        "product_id": line.product_id.id,
                        "name": line.product_id.display_name,
                        "quantity": line.quantity_to_invoice,
                        "price_unit": line.product_id.lst_price,
                    },
                )
            )

        move = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner_id.id,
                "journal_id": self.journal_id.id,
                "invoice_date": self.invoice_date,
                "invoice_line_ids": invoice_line_commands,
                "invoice_origin": batch.name,
            }
        )

        for line in lines_to_invoice:
            invoice_line = move.invoice_line_ids.filtered(lambda ml: ml.product_id == line.product_id)[:1]
            self.env["rc.invoice.batch.trace"].create(
                {
                    "batch_id": batch.id,
                    "batch_line_id": line.id,
                    "move_id": move.id,
                    "move_line_id": invoice_line.id,
                    "quantity": line.quantity_to_invoice,
                }
            )
            line.quantity_to_invoice = 0.0

        if all(l.quantity_available <= 0 for l in batch.line_ids):
            batch.state = "invoiced"

        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": move.id,
            "target": "current",
        }
