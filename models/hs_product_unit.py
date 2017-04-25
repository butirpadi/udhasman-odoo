from odoo import api, models, fields

class hs_product_unit(models.Model):
	_name = 'hs.product.unit'

	name = fields.Char('Nama')
