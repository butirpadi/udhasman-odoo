from odoo import api, fields, models, osv
from pprint import pprint

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
				], string='Kalkulasi')
	quantity = fields.Integer('Quantity', default=1)
	panjang = fields.Float('Panjang')
	lebar = fields.Float('Lebar')
	tinggi = fields.Float('Tinggi')
	volume = fields.Float('Volume')
	gross = fields.Float('Gross')
	tare = fields.Float('Tare')
	netto = fields.Float('Netto')
	harga_satuan = fields.Float('Unit Price')
	harga_total = fields.Float('Total')
	status_nota_timbang = fields.Selection([('draft','Draft'),('open','Open'),('done','Done')],
									string='Status Nota Timbang', default='draft')

	# sale_order_id = fields.Many2one(
	#     'sale.order',
	#     string='Sales Order',
	# )

	# action set status nota timbang
	def action_validate_nota_timbang(self):
		print('Validate Nota Timbang')
		if self.kalkulasi and self.status_nota_timbang == 'open' :
			self.status_nota_timbang = 'done'
			# validate picking/delivery
			print('Validate picking')
			for pick in self.picking_ids:
				# set qt_done
				for operation in pick.pack_operation_product_ids:
					operation.qty_done = operation.product_qty
				# validate picking
				pick.do_new_transfer()
		else:
			print('Nota timbang already validated atau dalam status "DRAFT"')


	@api.onchange('kalkulasi')
	def onchange_kalkulasi(self):
		# clear input
		self.panjang = 0
		self.lebar = 0
		self.tinggi = 0
		self.volume = 0
		self.gross = 0
		self.tare = 0
		self.netto = 0
		# update order_line kalkulasi
		for line in self.order_line:
			line.kalkulasi = self.kalkulasi 


	# hitung kalkulasi kubikasi
	@api.onchange('panjang')
	def onchange_panjang(self):
		vol = 0
		vol = self.panjang * self.lebar * self.tinggi
		self.volume = vol 
		self.hitung_harga_total()

	@api.onchange('lebar')
	def onchange_lebar(self):
		vol = 0
		vol = self.panjang * self.lebar * self.tinggi
		self.volume = vol 
		self.hitung_harga_total()

	@api.onchange('tinggi')
	def onchange_tinggi(self):
		vol = 0
		vol = self.panjang * self.lebar * self.tinggi
		self.volume = vol 
		self.hitung_harga_total()

	@api.onchange('gross')
	def onchange_gross(self):
		net = 0
		net = self.gross - self.tare
		self.netto = net
		self.hitung_harga_total()

	@api.onchange('tare')
	def onchange_tare(self):
		net = 0
		net = self.gross - self.tare
		self.netto = net	 
		self.hitung_harga_total()

	@api.onchange('harga_satuan')
	def onchange_harga_satuan(self):
		self.hitung_harga_total()

	# Hitung harga total
	def hitung_harga_total(self):
		ord_qty = 1
		if(self.kalkulasi == 'ritase'):
			self.harga_total = self.harga_satuan 
			# update qty_delivered
			# self.qty_delivered =  
		elif(self.kalkulasi == 'kubikasi'):
			self.harga_total = self.volume * self.harga_satuan
			# update qty_delivered
			self.qty_delivered = self.volume
			ord_qty = self.volume
		elif(self.kalkulasi == 'tonase'):
			self.harga_total = self.netto * self.harga_satuan
			# update qty_delivered
			self.qty_delivered = self.netto 
			ord_qty = self.netto

		# update unit price 
		for line in self.order_line:
			line.price_unit = self.harga_satuan
			# line.kalkulasi = self.kalkulasi
			# set qty
			if(line.kalkulasi == 'ritase'):
				line.product_uom_qty = 1
				line.quantity = 1
			elif(line.kalkulasi == 'kubikasi'):
				line.product_uom_qty = self.volume
				line.volume = self.volume
			elif(line.kalkulasi == 'tonase'):
				line.product_uom_qty = self.netto
				line.netto = self.netto

		# update picking
		# print('list of picking')
		# for pick in self.picking_ids:
		# 	for move in pick.move_lines:
		# 		# print('move_line : ')
		# 		# pprint(move.name)
		# 		# pprint(move.ordered_qty)
		# 		# pprint(move.product_qty)
		# 		# pprint(move.remaining_qty)
		# 		# pprint(move.state)
		# 		# print('----------------------')
		# 		# update stock picking remaining
		# 		# move.ordered_qty = ord_qty
		# 		# move.product_qty = ord_qty
		# 		# move.remaining_qty = 0
		# 		move.write({
		# 				'ordered_qty':ord_qty,
		# 				'product_qty':ord_qty,
		# 				'remaining_qty':ord_qty,
		# 			})


		# 	# calculate price_total
			line._compute_amount()
			

	@api.model 
	def _compute_get_status_nota_timbang(self):
		self.status_nota_timbang
		# res = 'draft'
		# # for data in self:
		# if self.nomor_nota_timbang and self.kalkulasi:
		# 	res = 'done'
		# self.status_nota_timbang = res

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
	@api.multi
	def write(self,vals):
		# print('Data Kalkulasi : ' + vals['kalkulasi'])
		# disini pasti ada perubahan
		# maka dari itu update harga unit_price
		# if vals['kalkulasi'] == 'ritase':

		# elif vals['kalkulasi'] == 'kubikasi':
		# elif vals['kalkulasi'] == 'tonase':
		# for line in vals['order_line']:
		# 	print('harga satuan before : ' + str(line.price_unit))
		# 	# update price_unit 
		# 	line.price_unit = vals['harga_satuan']
		# 	print('Harga satuan after : ' + str(line.price_unit))
		# pprint(vals)

		# update status nota timbang
		# if self.kalkulasi:
		# 	print(self.status_nota_timbang)
		# 	self.status_nota_timbang = 'open'
		# 	print(self.status_nota_timbang)

		# pprint(vals)

		if 'kalkulasi' in vals:
			if vals['kalkulasi']:
				vals.update({'status_nota_timbang':'open'})

		return super(hs_sale_order,self).write(vals)
