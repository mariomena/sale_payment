from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleMakePayment(models.TransientModel):
    _name = "sale.make.payment"
    _description = "Sale Make Payment"

    journal_id = fields.Many2one(
        "account.journal",
        string="Journal",
        required=True,
        domain="[ ('type', 'in', ('bank', 'cash'))]",
    )
    amount = fields.Monetary(string="Amount", required=True)
    payment_date = fields.Date(string="Payment Date", default=fields.Date.context_today, required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id)

    def create_payment(self):
        active_id = self.env.context.get("active_id")
        if not active_id:
            return
        sale_order = self.env["sale.order"].browse(active_id)
        if not sale_order:
            return

        payment_vals = {
            "date": self.payment_date,
            "amount": self.amount,
            "payment_type": "inbound",
            "partner_type": "customer",
            "ref": sale_order.name,
            "journal_id": self.journal_id.id,
            "currency_id": self.currency_id.id,
            "partner_id": sale_order.partner_id.id,
            "sale_order_id": sale_order.id,
        }

        payment = self.env["account.payment"].create(payment_vals)
        payment.action_post()

        return {"type": "ir.actions.act_window_close"}
