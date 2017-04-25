from odoo import api, fields, models

class hs_stock_picking(models.Model):
	_inherit = "stock.picking"

	karyawan_id = fields.Many2one(
		'hs.karyawan',
		string='Driver',
	)
	