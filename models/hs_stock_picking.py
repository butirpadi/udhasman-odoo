from odoo import api, fields, models

class hs_stock_picking(models.Model):
	_inherit = "stock.picking"
	_order = 'id desc'

	karyawan_id = fields.Many2one('hs.karyawan', string='Driver')
	lokasi_galian_id = fields.Many2one('hs.lokasi.galian', string="Lokasi Galian")
	pekerjaan = fields.Char('Pekerjaan', compute="_compute_get_pekerjaan", store=True)
	pekerjaan_id = fields.Many2one( 'hs.pekerjaan',compute="_compute_get_pekerjaan_id",string="Pekerjaan", store=True,)
	
	min_date = fields.Datetime(
        'Delivery Date', compute='_compute_dates', inverse='_set_min_date', store=True,
        index=True, track_visibility='onchange',
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        help="Scheduled time for the first part of the shipment to be processed. Setting manually a value here would set it as expected date for all the stock moves.")

	kalkulasi = fields.Selection([
					('ritase','RITASE'),
					('kubikasi','KUBIKASI'),
					('tonase','TONASE')
				], related="move_lines.procurement_id.sale_line_id.order_id.kalkulasi", string='Kalkulasi', store=True)
	

	@api.depends('karyawan_id')
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

	@api.depends('karyawan_id')
	def _compute_get_pekerjaan_id(self):
		for pick in self:
			stock_move = pick.move_lines[0]
			procurement = stock_move.procurement_id
			sale_order_line = procurement.sale_line_id
			sale_order = sale_order_line.order_id
			pick.pekerjaan_id = sale_order.pekerjaan_id
	