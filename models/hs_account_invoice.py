from odoo import api, fields, models
from pprint import pprint

class hs_purchase(models.Model):
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