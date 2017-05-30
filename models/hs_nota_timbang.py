from odoo import api, models, fields 

class hs_nota_timbang(models.Model):
	_name = "hs.nota.timbang"

	name = fields.Char('Nomor Nota')
	kalkulasi = fields.Selection([
					('ritase','RITASE'),
					('kubikasi','KUBIKASI'),
					('tonase','TONASE')
				], string='Kalkulasi',required=True,default='ritase')
	quantity = fields.Integer('Quantity')
	panjang = fields.Float('Panjang')
	lebar = fields.Float('Lebar')
	tinggi = fields.Float('Tinggi')
	volume = fields.Float('Volume', readonly=True)
	gross = fields.Float('Gross')
	tare = fields.Float('Tare')
	netto = fields.Float('Netto', readonly=True)

	sale_order_id = fields.Many2one(
	    'sale.order',
	    string='Sales Order',
	)