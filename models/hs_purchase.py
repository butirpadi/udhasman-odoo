from odoo import api, fields, models
from pprint import pprint

class hs_purchase(models.Model):
	_inherit = "purchase.order"


	# @api.model
	# def create(self, vals):
	# 	print('CETAK DATA =======================================================')
	# 	print(var(self))
	# 	newrow = super(hs_purchase,self).create(vals)
	# 	return newrow

	# Override Button_confirm	
	@api.multi
	def button_confirm(self):	
		res =  super(hs_purchase,self).button_confirm()
		
		# CEK APAKAH MENGGUNAKAN ONE STEP PURCHASING
		is_one_step_purchase = self.env['ir.config_parameter'].get_param('one_step_purchasing')

		if is_one_step_purchase == 'True':
			print('ONE STEP PURCHASE ENABLED')
			# Auto Generate Picking/Receive Shiptment 
			picking = self.picking_ids[0]
			for dt in picking:
				# loop ke detail produk nya
				for prd in dt.pack_operation_product_ids:
					prd.qty_done = prd.product_qty
			picking.do_new_transfer()

			# accinv = AccountInvoice()
			# self.pool.get('account.invoice').create(accinv,{'purchase_id':self.id})
			hs_invoice_line_ids = []
			for prod in self.order_line:
				print prod.product_id.name +  " " + str(prod.product_id.id)
				print prod.price_unit
				print prod.price_subtotal
				detail_inv_line = { 'account_analytic_id': False,
			                         'account_id': 19,
			                         'analytic_tag_ids': [[5]],
			                         'discount': 0,
			                         'invoice_line_tax_ids': [[5]],
			                         'name': self.name + ': ' + prod.product_id.name, #'PO00002: BUCKET GP 251-1778',
			                         'price_subtotal': prod.price_subtotal,
			                         'price_unit': prod.price_unit,
			                         'product_id': prod.product_id.id,
			                         'purchase_id': self.id,
			                         'purchase_line_id': prod.id,
			                         'quantity': prod.product_qty,
			                         # 'sequence': 0,
			                         'uom_id': 1
			                         }
				hs_invoice_line_ids.append([0,False,detail_inv_line])

				# update qty_invoiced
				print('Update QTY_INVOICED')
				prod.write({'qty_invoiced':prod.product_qty})
				# update status invoiced
				print('Update INVOICED status')
				self._get_invoiced()

			
			print('===============================')
			print('DETAIL INVOICE LINES')
			print('===============================')
			pprint(hs_invoice_line_ids)

			journal_domain = [
					('type', '=', 'purchase'),
					('company_id', '=', self.company_id.id),
					('currency_id', '=', self.currency_id.id),
				]
			default_journal_id = 2

			# update qty_invoiced pada tabel purchase_order_lines

			invoice_vals = {'account_id': 13,
							 'comment': False,
							 'company_id': self.company_id.id,
	 						 'currency_id': self.currency_id.id,
							 'date': False,
							 'date_due': False,
							 'date_invoice': False,
							 'fiscal_position_id': False,
							 'invoice_line_ids': hs_invoice_line_ids,
							 'journal_id': default_journal_id,
							 'message_follower_ids': False,
							 'message_ids': False,
							 'move_name': False,
							 'name': False,
							 'origin': self.name,
							 'partner_bank_id': False,
							 'partner_id': self.partner_id.id,
							 'payment_term_id': False,
							 'purchase_id': self.id,
							 'reference': False,
							 'tax_line_ids': [],
							 'user_id': 1,
							 'type':'in_invoice',
							 'default_purchase_id': self.id};

			print('===============================')
			print('INVOICE VALS')
			print('===============================')
			pprint(invoice_vals)
			accinv = self.env['account.invoice']
			print('GENERATING INVOICE')
			accinv.create(invoice_vals)
			print('VALIDATE INVOICE')
			the_invoice = self.invoice_ids[0]
			the_invoice.action_invoice_open()
			print('GENERATE INVOICE DONE')
		else:
			print('ONE STEP PURCHASE DISABLED')

		return res

	# Get Shipment Number
	@api.one
	def _compute_get_shipment_number(self):
		hs_pickng_id = '-'
		if self.state != 'draft' and self.state != 'cancel':
			hs_pickng_id = self.picking_ids[0].name
		self.input_temp = hs_pickng_id

	# Testing get temp data
	@api.model
	def _compute_get_temp_value(self):
		self.input_temp = self.env['ir.config_parameter'].get_param('web.base.url')


	state = fields.Selection([
	        ('draft', 'Draft'),
	        ('sent', 'RFQ Sent'),
	        ('to approve', 'To Approve'),
	        ('purchase', 'Purchase Order'),
	        ('done', 'Locked'),
	        ('cancel', 'Cancelled')
	        ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
	input_temp  = fields.Char('Temp Field',compute="_compute_get_temp_value")

