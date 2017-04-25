from odoo import models, api, fields 

class hs_pekerjaan(models.Model):
	_name = "hs.pekerjaan"

	name = fields.Char('Nama', required=True)
	partner_id = fields.Many2one('res.partner', string='Customer', required=True)
	tahun = fields.Char('Tahun',size=4, required=True)
	alamat = fields.Char('Alamat')
	provinsi_id = fields.Many2one('hs.provinsi', 'Provinsi')
	kabupaten_id = fields.Many2one('hs.kabupaten', 'Kabupaten')
	kecamatan_id = fields.Many2one('hs.kecamatan', 'Kecamatan')