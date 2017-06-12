from odoo import api, models, fields

class hs_presensi_karyawan(models.Model):
	_name = "hs.presensi_karyawan_rel"

	name = fields.Char('Reference')
	presensi_id = fields.Many2one('hs.presensi', string='Presensi', ondelete='cascade')
	karyawan_id = fields.Many2one('hs.karyawan', string='Karyawan')
	pagi = fields.Boolean('Pagi')
	siang = fields.Boolean('Siang')
	tanggal = fields.Date(related="presensi_id.tanggal",string="Tanggal")