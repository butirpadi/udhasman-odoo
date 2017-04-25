from odoo import api, models, fields
from pprint import pprint

class hs_product_change_quantity(models.TransientModel):
    _inherit = "stock.change.product.qty"
    
    @api.model 
    def create(self, vals):
    	print('DATA PRODUCT CHANGE VALS')
    	print('==================================')
    	pprint(vals)
    	newrow = super(ProductChangeQuantity,self).create(vals)

    	return newrow