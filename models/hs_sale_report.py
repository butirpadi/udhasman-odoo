from odoo import models, fields, api

class hs_sale_report(models.TransientModel):
	_name = 'hs_sale_report'

	tanggal_awal = fields.Date('Tanggal Awal', required=True,)
	tanggal_akhir = fields.Date('Tanggal Akhir', required=True,)
	sale_order_ids = fields.One2many('sale.order', string="Sale Order")