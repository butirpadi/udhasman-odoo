from odoo import api, fields, models

class hs_stock_picking(models.Model):
	_inherit = "stock.picking"

	karyawan_id = fields.Many2one('hs.karyawan', string='Driver')
	lokasi_galian_id = fields.Many2one('hs.lokasi.galian', string="Lokasi Galian")
	pekerjaan = fields.Char('Pekerjaan', compute="_compute_get_pekerjaan", store=True)
	min_date = fields.Datetime(
        'Delivery Date', compute='_compute_dates', inverse='_set_min_date', store=True,
        index=True, track_visibility='onchange',
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        help="Scheduled time for the first part of the shipment to be processed. Setting manually a value here would set it as expected date for all the stock moves.")

	@api.depends('karyawan_id')
	def _compute_get_pekerjaan(self):
		for pick in self:
			if pick.origin:
				orders = self.env['sale.order'].search([('name','=',pick.origin)])
				for order in orders:
					if order.pekerjaan_id:
						pick.pekerjaan = order.pekerjaan_id.name
					else:
						pick.pekerjaan = "-"
	