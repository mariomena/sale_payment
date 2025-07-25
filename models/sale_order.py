from odoo import _, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_ids = fields.One2many(
        "account.payment",
        "sale_order_id",
        string="Payments",
        readonly=True,
        copy=False,
    )

    def action_open_register_payment_wizard(self):
        return {
            "name": _("Register Payment"),
            "type": "ir.actions.act_window",
            "res_model": "sale.make.payment",
            "view_mode": "form",
            "target": "new",
            "context": {"active_model": "sale.order", "active_id": self.id},
        }

    def _create_invoices(self, grouped=False, final=False, date=None):
        invoices = super()._create_invoices(grouped, final, date)
        for order in self:
            if order.payment_ids:
                for invoice in invoices:
                    for payment in order.payment_ids:
                        if payment.state == "posted":
                            invoice.js_assign_outstanding_line(payment.move_id.line_ids.filtered(lambda x: x.account_id.account_type == 'asset_receivable'))
        return invoices
