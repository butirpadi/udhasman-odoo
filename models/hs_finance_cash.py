from odoo import api, fields, models
from pprint import pprint

class hs_finance_cash(models.Model):
	_name = "hs.finance.cash"
	_order = 'tanggal desc, id desc'

	name = fields.Char(string='Cash Number', required=True, copy=False, readonly=True, 
    					index=True, select=True, default='New')
	keterangan = fields.Char('Keterangan', required=True,)
	tanggal = fields.Date('Tanggal', required=True)
	tipe = fields.Selection([
        ('debet', 'Debet'),
        ('credit', 'Credit'),
        ], string="Tipe", required=True,)
	jumlah = fields.Float('Jumlah', required=True, default=0.0)

	debet = fields.Float('Debet',compute="_compute_get_debet", store=True)
	kredit = fields.Float('Kredit',compute="_compute_get_kredit", store=True)

	def _compute_get_debet(self):
		for fin in self:
			if fin.tipe == 'debet':
				fin.debet = fin.jumlah

	def _compute_get_kredit(self):
		for fin in self:
			if fin.tipe == 'credit':
				fin.kredit = fin.jumlah

	@api.model
	def create(self, vals):
		if vals.get('name', ('New')) == ('New'):
			if vals['tipe'] == 'debet':
				vals['name'] = self.env['ir.sequence'].next_by_code('hs.finance.cash.in') or ('New')
			else:
				vals['name'] = self.env['ir.sequence'].next_by_code('hs.finance.cash.out') or ('New')
	
		result = super(hs_finance_cash, self).create(vals)
		return result
    