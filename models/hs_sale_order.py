from odoo import api, fields, models, osv

class hs_sale_order(models.Model):
	_inherit = 'sale.order'

	# data pekerjaan dari setiap orderan
	pekerjaan_id = fields.Many2one(
	    'hs.pekerjaan',
	    string='Pekerjaan'
	)

	# nota timbang
	# nota_timbang_id = fields.One2many(
	#     'hs.nota.timbang',
	#     'sale_order_id',
	#     string='Nota Timbang',
	# )

	# nota_timbang_count = fields.Integer(
	#     'Nota Timbang',
	#     compute = "_compute_get_nota_timbang_count"
	# )

	# @api.model
	# def _compute_get_nota_timbang_count(self):
	# 	for data in self:
	# 		data.nota_timbang_count = 1

	nomor_nota_timbang = fields.Char('Nomor Nota')
	kalkulasi = fields.Selection([
					('ritase','RITASE'),
					('kubikasi','KUBIKASI'),
					('tonase','TONASE')
				], string='Kalkulasi',required=True, default='ritase')
	quantity = fields.Integer('Quantity')
	panjang = fields.Float('Panjang')
	lebar = fields.Float('Lebar')
	tinggi = fields.Float('Tinggi')
	volume = fields.Float('Volume')
	gross = fields.Float('Gross')
	tare = fields.Float('Tare')
	netto = fields.Float('Netto')
	harga_satuan = fields.Float('Unit Price')
	harga_total = fields.Float('Total')
	nota_timbang_status = fields.Char('Status Nota Timbang',compute="_compute_get_status_nota_timbang")

	@api.onchange('kalkulasi')
	def onchange_kalkulasi(self):
		self.panjang = 0
		self.lebar = 0
		self.tinggi = 0
		self.volume = 0
		self.gross = 0
		self.tare = 0
		self.netto = 0

	# hitung kalkulasi kubikasi
	@api.onchange('panjang')
	def onchange_panjang(self):
		vol = 0
		vol = self.panjang * self.lebar * self.tinggi
		self.volume = vol 

	@api.onchange('lebar')
	def onchange_lebar(self):
		vol = 0
		vol = self.panjang * self.lebar * self.tinggi
		self.volume = vol 

	@api.onchange('tinggi')
	def onchange_tinggi(self):
		vol = 0
		vol = self.panjang * self.lebar * self.tinggi
		self.volume = vol 


	@api.model 
	def _compute_get_status_nota_timbang(self):
		res = False
		for data in self:
			if data.nota_timbang and data.kalkulasi:
				res = True

		return res

	sale_order_id = fields.Many2one(
	    'sale.order',
	    string='Sales Order',
	)

	# Tampilkan form nota timbang
	@api.multi
	def action_view_nota_timbang(self):
		nota_tbg = self.mapped('nota_timbang_id')
		action = self.env.ref('hs_nota_timbang_tree').read()[0]

		if len(nota_tbg) == 1:
			action['views'] = [(self.env.ref('hs_nota_timbang_form').id, 'form')]
			action['res_id'] = nota_tbg.ids[0]
		else:
			action = {'type': 'ir.actions.act_window_close'}
		
		return action

	# show driver name
	driver = fields.Char('Driver',compute='_compute_get_delivery_driver', readonly=True )

	picking_status = fields.Selection([
        ('draft', 'Draft'), ('cancel', 'Cancelled'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting Availability'),
        ('partially_available', 'Partially Available'),
        ('assigned', 'Available'), ('done', 'Done')],
        string='Delivery Status', compute='_compute_get_picking_status', readonly=True)
	
	@api.model 
	def _compute_get_delivery_driver(self):
		for data in self:
			if len(data.picking_ids) > 0 :
				for pick in data.picking_ids:
				# print(pick.karyawan_id.armada_id.name)
					if pick.karyawan_id.armada_id.name and pick.karyawan_id.name :
						data.driver = pick.karyawan_id.armada_id.name + " - " + pick.karyawan_id.name  
					else:
						data.driver = "-"
					# data.driver = pick.karyawan_id.name  
			else:
				data.driver = "-"

	@api.model
	def _compute_get_picking_status(self):
		# print active_id
		for data in self:
			for pick in data.picking_ids:
				# print(pick.karyawan_id.armada_id.name)
				data.picking_status = pick.state


	@api.onchange('order_line')
	def cek_order_line_length(self):
		if len(self.order_line) > 1:
			return {'value':{},'warning':{'title':'warning','message':'Hanya boleh 1 product saja'}}


	# override method write
	# @api.multi
	# def write(self,vals):
	# 	print('Update Data Sales Order')
	# 	# Update volume atau netto
	# 	if self.kalkulasi == 'kubikasi':
	# 		vol = self.panjang * self.lebar * self.tinggi
	# 		# self.volume = vol
	# 		print('VOL : ' + str(vol))
	# 		print('self.VOLUME : ' + str(self.volume))
	# 		vals.update({'volume':vol})
	# 		print('self.VOLUME.after : ' + str(self.volume))
	# 	if self.kalkulasi == 'tonase':
	# 		net = self.gross - self.tare
	# 		# self.netto = net
	# 		print('NET : ' + str(net))
	# 		print('self.NETTO : ' + str(self.netto))
	# 		vals.update({'netto':net})
	# 		print('self.NETTO.after : ' + str(self.netto))

	# 	return super(hs_sale_order,self).write(vals)
