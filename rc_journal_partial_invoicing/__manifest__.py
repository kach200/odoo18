{
    "name": "RC Journal Partial Invoicing",
    "summary": "Acumula productos vendidos por diario y permite facturacion parcial controlada.",
    "version": "18.0.1.0.0",
    "category": "Accounting",
    "author": "Custom",
    "license": "LGPL-3",
    "depends": ["account"],
    "data": [
        "data/rc_invoice_batch_sequence.xml",
        "security/ir.model.access.csv",
        "views/rc_invoice_batch_views.xml",
        "views/rc_generate_invoice_wizard_views.xml"
    ],
    "installable": True,
    "application": False
}
