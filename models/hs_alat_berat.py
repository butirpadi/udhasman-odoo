from odoo import api, models, fields

class hs_alat_berat(models.Model):
	_name = "hs.alat_berat"

	name = fields.Char(
	    string='Nama',
	)
	kode = fields.Char(
		String='Kode'
	)

