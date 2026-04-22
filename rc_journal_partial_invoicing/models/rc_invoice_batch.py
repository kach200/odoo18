from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class RcInvoiceBatch(models.Model):
    _name = "rc.invoice.batch"
    _description = "Lote de facturacion por diario"
    _order = "id desc"

    name = fields.Char(string="Referencia", required=True, copy=False, default=lambda self: _("Nuevo"))
    source_journal_id = fields.Many2one(
        "account.journal",
        string="Diario origen",
        required=True,
        domain=[("type", "=", "sale")],
    )
    target_journal_id = fields.Many2one(
        "account.journal",
        string="Diario destino factura",
        required=True,
        domain=[("type", "=", "sale")],
    )
    date_from = fields.Date(string="Desde")
    date_to = fields.Date(string="Hasta")
    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("ready", "Listo"),
            ("invoiced", "Facturado"),
        ],
        default="draft",
        string="Estado",
    )
    line_ids = fields.One2many("rc.invoice.batch.line", "batch_id", string="Lineas")
    can_generate_invoice = fields.Boolean(compute="_compute_can_generate_invoice")
    invoice_count = fields.Integer(compute="_compute_invoice_count")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("Nuevo")) == _("Nuevo"):
                vals["name"] = self.env["ir.sequence"].next_by_code("rc.invoice.batch") or _("Nuevo")
        return super().create(vals_list)

    @api.depends("line_ids.quantity_to_invoice")
    def _compute_can_generate_invoice(self):
        for batch in self:
            batch.can_generate_invoice = any(line.quantity_to_invoice > 0 for line in batch.line_ids)

    def _compute_invoice_count(self):
        for batch in self:
            move_ids = batch.line_ids.mapped("trace_ids.move_id.id")
            batch.invoice_count = len(set(move_ids))

    @api.constrains("date_from", "date_to")
    def _check_dates(self):
        for batch in self:
            if batch.date_from and batch.date_to and batch.date_from > batch.date_to:
                raise ValidationError(_("La fecha desde no puede ser mayor que la fecha hasta."))

    def action_load_lines(self):
        self.ensure_one()
        domain = [
            ("move_id.move_type", "=", "out_invoice"),
            ("move_id.state", "=", "posted"),
            ("move_id.journal_id", "=", self.source_journal_id.id),
            ("display_type", "=", False),
            ("product_id", "!=", False),
        ]
        if self.date_from:
            domain.append(("move_id.invoice_date", ">=", self.date_from))
        if self.date_to:
            domain.append(("move_id.invoice_date", "<=", self.date_to))

        grouped = self.env["account.move.line"].read_group(
            domain,
            ["product_id", "quantity:sum"],
            ["product_id"],
            lazy=False,
        )

        self.line_ids.unlink()
        line_values = []
        for item in grouped:
            product = item.get("product_id")
            if not product:
                continue
            sold_qty = item.get("quantity", 0.0)
            if sold_qty <= 0:
                continue
            line_values.append(
                {
                    "batch_id": self.id,
                    "product_id": product[0],
                    "quantity_sold": sold_qty,
                }
            )
        self.env["rc.invoice.batch.line"].create(line_values)
        self.state = "ready"
        return True

    def action_open_generate_wizard(self):
        self.ensure_one()
        if not self.can_generate_invoice:
            raise UserError(_("Debes ingresar una cantidad a facturar en al menos una linea."))

        return {
            "type": "ir.actions.act_window",
            "res_model": "rc.generate.invoice.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_batch_id": self.id,
                "default_journal_id": self.target_journal_id.id,
            },
        }

    def action_view_invoices(self):
        self.ensure_one()
        move_ids = self.env["rc.invoice.batch.trace"].search([("batch_id", "=", self.id)]).mapped("move_id").ids
        return {
            "type": "ir.actions.act_window",
            "name": _("Facturas generadas"),
            "res_model": "account.move",
            "view_mode": "list,form",
            "domain": [("id", "in", move_ids)],
            "context": {"create": False},
        }


class RcInvoiceBatchLine(models.Model):
    _name = "rc.invoice.batch.line"
    _description = "Linea acumulada para facturacion"

    batch_id = fields.Many2one("rc.invoice.batch", string="Lote", required=True, ondelete="cascade")
    product_id = fields.Many2one("product.product", string="Producto", required=True)
    quantity_sold = fields.Float(string="Cantidad vendida", required=True)
    quantity_invoiced = fields.Float(string="Cantidad ya facturada", compute="_compute_quantities", store=True)
    quantity_available = fields.Float(string="Cantidad disponible", compute="_compute_quantities", store=True)
    quantity_to_invoice = fields.Float(string="A facturar")
    trace_ids = fields.One2many("rc.invoice.batch.trace", "batch_line_id", string="Trazas")

    _sql_constraints = [
        (
            "batch_product_unique",
            "unique(batch_id, product_id)",
            "No se puede repetir el mismo producto dentro del lote.",
        )
    ]

    @api.depends("quantity_sold", "trace_ids.quantity")
    def _compute_quantities(self):
        for line in self:
            invoiced = sum(line.trace_ids.mapped("quantity"))
            line.quantity_invoiced = invoiced
            line.quantity_available = max(line.quantity_sold - invoiced, 0.0)

    @api.constrains("quantity_to_invoice")
    def _check_quantity_to_invoice(self):
        for line in self:
            if line.quantity_to_invoice < 0:
                raise ValidationError(_("La cantidad a facturar no puede ser negativa."))
            if line.quantity_to_invoice > line.quantity_available:
                raise ValidationError(
                    _("La cantidad a facturar no puede ser mayor que la cantidad disponible.")
                )


class RcInvoiceBatchTrace(models.Model):
    _name = "rc.invoice.batch.trace"
    _description = "Traza de facturacion por lote"
    _order = "id desc"

    batch_id = fields.Many2one("rc.invoice.batch", string="Lote", required=True, ondelete="cascade")
    batch_line_id = fields.Many2one("rc.invoice.batch.line", string="Linea lote", required=True, ondelete="cascade")
    move_id = fields.Many2one("account.move", string="Factura", required=True, ondelete="cascade")
    move_line_id = fields.Many2one("account.move.line", string="Linea factura", required=True, ondelete="cascade")
    quantity = fields.Float(string="Cantidad", required=True)
