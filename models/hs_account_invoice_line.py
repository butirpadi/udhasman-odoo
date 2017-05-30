from odoo import api, fields, models
from pprint import pprint

class hs_account_invoice_line(models.Model):
    _inherit = "account.invoice.line"

    sale_order_lines = fields.Many2many('sale.order.line', 
										'sale_order_line_invoice_rel', 
										'invoice_line_id', 'order_line_id', 
										'Sale Order  Lines', 
										readonly=True)