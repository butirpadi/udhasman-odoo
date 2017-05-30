from odoo import api, fields, models, osv, tools
import datetime
import timestring
import pytz
from pprint import pprint

class hs_sale_order(models.Model):
	_inherit = 'sale.order'

	# data pekerjaan dari setiap orderan
	pekerjaan_id = fields.Many2one(
	    'hs.pekerjaan',
	    string='Pekerjaan'
	)

	material = fields.Char('Material',compute="_compute_get_material", store=True)
	@api.depends('order_line')
	def _compute_get_material(self):
		for so in self:
			for line in so.order_line:
				if line.product_id:
					 so.material = line.product_id.name
				else:
					 so.material = '-'


	# override date_order, change datetime to date
	# date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, 
	# 	states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, 
	# 	copy=False, default=fields.Datetime.now)


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
	status_nota_timbang = fields.Selection([
									('draft','Draft'),
									('open','Open'),
									('done','Done')
									], string='Status Nota Timbang', default='draft')
	# invoice_status = fields.Selection([
 #        ('upselling', 'Upselling Opportunity'),
 #        ('invoiced', 'Fully Invoiced'),
 #        ('to invoice', 'To Invoice'),
 #        ('no', 'Nothing to Invoice')
 #        ], string='Invoice Status', compute='_compute_get_invoice_status', store=True)

	# # compute get invoice status
	# def _compute_get_invoice_status(self):
	# 	print('Inside compute get invoice status')
	# 	inv_sts = None
	# 	for line in self.order_line:
	# 		print ('Status invoice : ' + line.invoice_status)
	# 		inv_sts = line.invoice_status
	# 	self.invoice_status = inv_sts

	# sale_order_id = fields.Many2one(
	#     'sale.order',
	#     string='Sales Order',
	# )

	@api.model
	def search(self, args, offset=0, limit=0, order=None, count=False):
		# pprint(args)
		# print('---------------------------------------------')

		DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
		akhir = ""
		awal = ""
		awal_utc_str = ""
		akhir_utc_str = ""
		for doms in args:
			if doms[0] in 'date_order':
				if doms[1] == '=':
					dt = timestring.Date(doms[2])
					# lokalisasi datetime
					localtz = pytz.timezone('Asia/Jakarta')	
					dt_local_str = pytz.utc.localize(datetime.datetime.strptime(doms[2], DATETIME_FORMAT)).astimezone(localtz).strftime(DATETIME_FORMAT)
					dt_local = timestring.Date(dt_local_str)
					awal = str(dt_local.date.date()) + ' ' + '00:00:00'
					akhir = str(dt_local.date.date()) + ' ' + '23:59:00'

					# set to UTC lagi
					awal_utc_str = localtz.localize(datetime.datetime.strptime(awal, DATETIME_FORMAT))
					awal_utc_str = awal_utc_str.astimezone(pytz.utc).strftime(DATETIME_FORMAT)

					akhir_utc_str = localtz.localize(datetime.datetime.strptime(akhir, DATETIME_FORMAT))
					akhir_utc_str = akhir_utc_str.astimezone(pytz.utc).strftime(DATETIME_FORMAT)
					
				# 	# doms = [('date_order','>=',awal),('date_order','<=',akhir)]
					doms[1] = '>='
					doms[2] = awal_utc_str
					# doms = ['date_order','>=',awal]
					args.append(['date_order','<=',akhir_utc_str])
				# 	print('=================================')
				# 	pprint(doms)
				# 	print('---------------------------------')
				# else:
				# 	print 'tidak ketemu'

		# append new filter
		
		# pprint(doms)
		   # if doms[0] in 'order_date':
		   #   kick me!
		   # else:
		   #   love me!
			# print(akhir)
			
			# print(localtz)
			# print(datetime.utcfromtimestamp(akhir))
		# print('awal :' + awal_utc_str)
		# print('akhir : ' + akhir_utc_str)
		# print('---------------------------------------------')
		# pprint(args)
		return super(hs_sale_order,self).search(args,offset,limit,order,count)

	# action set status nota timbang
	def action_validate_nota_timbang(self):
		print('Validate Nota Timbang')
		if self.kalkulasi and self.status_nota_timbang == 'open' :
			# # check has picking
			# set status nota timbang to done
			self.status_nota_timbang = 'done'
			# validate picking/delivery
			print('Validate picking')
			for pick in self.picking_ids:
				# set qt_done
				for operation in pick.pack_operation_product_ids:
					operation.qty_done = operation.product_qty
				# validate picking
				pick.do_new_transfer()

			for line in self.order_line:
				# reset quantity of product
				print('Reset quantity')
				print('=======================================')
				Inventory = self.env['stock.inventory']
				inventory = Inventory.create({
					'name': ('INV: %s') % tools.ustr(line.product_id.name),
					'filter': 'product',
					'product_id': line.product_id.id,
					'location_id': 15,
					# 'lot_id': wizard.lot_id.id,
					'line_ids': [(0, 0, {
				               'product_qty': 350,
				               'location_id': 15,
				               'product_id': line.product_id.id,
				               # 'product_uom_id': self.product_id.uom_id.id,
				               'theoretical_qty': 350,
				               # 'prod_lot_id': self.lot_id.id,
				        })],
				})
				inventory.action_done() 
				print('Reset Quantity Done')
		else:
			print('Nota timbang already validated atau dalam status "DRAFT"')


	# function to reset sale order & regenerate picking 
	def reset_sale_order(self):
		# set nota timbang status to draft
		self.status_nota_timbang = 'draft'
		self.kalkulasi = None
		self.panjang = None
		self.lebar = None
		self.tinggi = None
		self.volume = None
		self.gross = None
		self.tare = None
		self.netto = None
		self.harga_satuan = None
		self.harga_total = None
		self.quantity = None
		# Delete Picking
		print('Validate picking')
		for pick in self.picking_ids:
			print('Check Backorder nya : ')
			if pick.check_backorder():
				# set operation state to available
				# set qt_done
				for operation in pick.pack_operation_product_ids:
					# operation.state = 'assigned'
					print('Operation State-nya : ' + operation.state)
					# reset product_qty
					if self.kalkulasi == 'kubikasi':
						operation.product_qty = self.volume
					elif self.kalkulasi == 'tonase':
						operation.product_qty = self.netto
					elif self.kalkulasi == 'ritase':
						operation.product_qty = 1
					# set qty done
					operation.qty_done = operation.product_qty

				print('delete backorder')
				# delete other backorders
				print('delete move lines')
				for move in pick.move_lines:
					# move.write({'state','assigned'})
					move.state = 'assigned'
					move.action_cancel()
					move.unlink()
				# print('do the transfer')		
		# Generrate new picking
		if len(self.picking_ids) == 0:
			#delete procurement
			for order_line in self.order_line:
				order_line.kalkulasi = None
				order_line.volume = None
				order_line.netto = None
				order_line.quantity = None
				order_line.harga_satuan = None
				order_line.harga_total = None
				order_line.price_unit = None
				order_line._compute_amount()
				for proc in order_line.procurement_ids:
					proc.write({'state':'confirmed'})
					proc.unlink()

			# unconfirm sale
			# self.state = 'draft'
			print('reset sale order state ')
			self.write({'state':'draft'})
		# Delete Invoices
		print('Deleting invoices')
		if len(self.invoice_ids) > 0:
			for inv in self.invoice_ids:
				print('delete invoice ' + inv.name)
				inv.write({'state':'draft'})
				# delete invoice move
				# inv.move_name = False
				inv.move_id.write({'state':'draft'})
				inv.move_id.unlink()
				# inv.move_id.unlink()
				inv.unlink()
				print('delete invoice ' + inv.name + ' done')

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
