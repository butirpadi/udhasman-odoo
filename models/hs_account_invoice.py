from odoo import api, fields, models
from pprint import pprint

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





