from odoo import api, fields, models
from pprint import pprint

class hs_account_payment(models.Model):
	_inherit = "account.payment"

	@api.onchange('journal_id')
	def onchange_jurnal_id(self):
		print('Jurnal ID Change')
		pprint(self.journal_id.id)

	journal_id = fields.Many2one('account.journal', 
					string='Payment Journal', required=True, 
					domain=[('type', 'in', ('bank', 'cash'))], default=6)

	@api.model
	def _compute_get_default_journal(self):
		journals = self.env['account.journal'].search([('type','=','cash')])
		return journals[0]