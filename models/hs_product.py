from odoo import api, models, fields, tools
from pprint import pprint

class hs_product(models.Model):
	_inherit = "product.template"

	tipe_product = fields.Selection([('part', 'Sparepart'), ('mtr','Material')], 'Tipe', required=True)
	empfield = fields.Char('Empty Field')
	product_unit_id = fields.Many2one('hs.product.unit','Satuan')

	@api.model
	def create(self, vals):
		# newrow = super(product_template,self).create(vals)
		## set jika tipe adalah part maka type adalah cons
		print('tipe produk : ' + vals['tipe_product'])
		if vals['tipe_product'] == 'part':
			vals.update({'type':'consu'})
			vals.update({'purchase_ok':True})
			vals.update({'sale_ok':False})
		elif vals['tipe_product'] == 'mtr':
			# vals.update({'type':'service'})
			vals.update({'type':'product'})
			vals.update({'sale_ok':True})
			vals.update({'purchase_ok':False})
			# add inital quantity
			# newval = {
			# 			'product_id' : vals
			# 		}
			# self.env['stock.change.product.qty'].
			# pprint(vals)
			# print('==========================')
			# print('DATA ID : ')
			# print('==========================')
			# print(vals['id'])

		newrow = super(hs_product,self).create(vals)

		# Tambahkan quantity jika produk jenis Material
		if vals['tipe_product'] == 'mtr':
			print('Add initial quantity')
			print('=======================================')
			Inventory = self.env['stock.inventory']
			inventory = Inventory.create({
				'name': ('INV: %s') % tools.ustr(newrow.name),
				'filter': 'product',
				'product_id': newrow.id,
				'location_id': 15,
				# 'lot_id': wizard.lot_id.id,
				'line_ids': [(0, 0, {
			               'product_qty': 350,
			               'location_id': 15,
			               'product_id': newrow.id,
			               # 'product_uom_id': self.product_id.uom_id.id,
			               'theoretical_qty': 350,
			               # 'prod_lot_id': self.lot_id.id,
			        })],
			})
			inventory.action_done()

		return newrow

