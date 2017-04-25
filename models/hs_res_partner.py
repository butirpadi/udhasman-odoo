from odoo import api, models, fields

class hs_res_partner(models.Model):
	_inherit = 'res.partner'

	provinsi_id = fields.Many2one('hs.provinsi', 'Provinsi')
	kabupaten_id = fields.Many2one('hs.kabupaten', 'Kabupaten')
	kecamatan_id = fields.Many2one('hs.kecamatan', 'Kecamatan')
	pekerjaan_ids = fields.One2many(
	    'hs.pekerjaan',
	    'partner_id',
	    string='Data Pekerjaan',
	)