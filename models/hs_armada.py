from odoo import api, models, fields

class hs_armada(models.Model):
	_name = "hs.armada"

	name = fields.Char(
	    string='Nopol',
	)
	keterangan = fields.Char(
	    string='Keterangan',
	)

