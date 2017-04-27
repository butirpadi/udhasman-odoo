from odoo import api, fields, models, osv
from pprint import pprint

class hs_sale_order_line(models.Model):
	_inherit = 'sale.order.line'

	kalkulasi = fields.Selection([
					('ritase','RITASE'),
					('kubikasi','KUBIKASI'),
					('tonase','TONASE')
				], string='Kalkulasi')
	quantity = fields.Integer('Quantity', default=1)
	volume = fields.Float('Volume')
	netto = fields.Float('Netto')
	harga_satuan = fields.Float('Unit Price')
	harga_total = fields.Float('Total')