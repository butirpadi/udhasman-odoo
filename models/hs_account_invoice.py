from odoo import api, fields, models
from pprint import pprint
import datetime
import timestring
import pytz

class hs_account_invoice(models.Model):
	_inherit = "account.invoice"

	@api.multi
	def _compute_get_journal(self):
		account_jurnal = self.env['account.journal'].search([('type','=','cash')])
		pprint(account_jurnal[0].id)
		self.data_jurnal = self.get_cash_journal_id()

	@api.multi
	def get_cash_journal_id(self):
		account_jurnal = self.env['account.journal'].search([('type','=','cash')])
		return account_jurnal[0].id

	data_jurnal = fields.Char('Data Jurnal',compute="_compute_get_journal")

	so_data = fields.Boolean('SO Data',compute="_compute_get_sales_data",default=False, store=True)
	@api.depends('invoice_line_ids')
	def _compute_get_sales_data(self):
		for inv in self:
			for invline in inv.invoice_line_ids:
				for soline in invline.sale_order_lines:
					if soline.name:
						inv.so_data = True

	so_data_text = fields.Char('SO Data Text',compute="_compute_get_sales_data_text", default=False, store=True)	
	@api.depends('invoice_line_ids')
	def _compute_get_sales_data_text(self):
		for inv in self:
			for invline in inv.invoice_line_ids:
				for soline in invline.sale_order_lines:
					if soline.name:
						inv.so_data_text = soline.order_id.name

	pekerjaan = fields.Char('Pekerjaan', compute="_compute_get_pekerjaan", store=True)
	@api.depends('state')
	def _compute_get_pekerjaan(self):
		for inv in self:
			for invline in inv.invoice_line_ids:
				for soline in invline.sale_order_lines:
					if soline.name:
						inv.pekerjaan = soline.order_id.pekerjaan_id.name

	material = fields.Char('Material', compute="_compute_get_material", store=True)
	@api.depends('state')
	def _compute_get_material(self):
		for inv in self:
			for invline in inv.invoice_line_ids:
				inv.material = invline.product_id.name

	lokasi_galian = fields.Char('Lokasi Galian', compute="_compute_get_lokasi_galian", store=True)
	@api.depends('state')
	def _compute_get_lokasi_galian(self):
		for inv in self:
			for invline in inv.invoice_line_ids:
				for soline in invline.sale_order_lines:
					for pick in soline.order_id.picking_ids:
						print pick.lokasi_galian_id.name
						inv.lokasi_galian = pick.lokasi_galian_id.name


	# override original method
	# di gunakan untuk meng-update data tanggal di sesuaikan dengan tanggal sale_order
	@api.multi
	def action_invoice_open(self):
		super(hs_account_invoice, self).action_invoice_open()
		print 'inside action_invoice_open'
		for inv in self:
			for invline in inv.invoice_line_ids:
				for soline in invline.sale_order_lines:
					so = soline.order_id
					date_order_utc = so.date_order

					# lokalisasi datetime
					DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
					localtz = pytz.timezone('Asia/Jakarta')
					date_order_local = pytz.utc.localize(datetime.datetime.strptime(date_order_utc, DATETIME_FORMAT)).astimezone(localtz)	
					dt_local_str = date_order_local.strftime(DATETIME_FORMAT)
					# dt_local = timestring.Date(dt_local_str)
					# awal = str(dt_local.date.date()) + ' ' + '00:00:00'
					# akhir = str(dt_local.date.date()) + ' ' + '23:59:00'

					# # set to UTC lagi
					# awal_utc_str = localtz.localize(datetime.datetime.strptime(awal, DATETIME_FORMAT))
					# awal_utc_str = awal_utc_str.astimezone(pytz.utc).strftime(DATETIME_FORMAT)

					# akhir_utc_str = localtz.localize(datetime.datetime.strptime(akhir, DATETIME_FORMAT))
					# akhir_utc_str = akhir_utc_str.astimezone(pytz.utc).strftime(DATETIME_FORMAT)

					self.write({'date_invoice': date_order_local})





