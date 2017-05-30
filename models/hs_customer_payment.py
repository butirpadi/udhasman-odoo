from odoo import api, models, fields

class hs_customer_payment(models.Model):
	_name = "hs.customer.payment"

	name = fields.Char(string='Payment Number', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
	state = fields.Selection([
        ('draft', 'Quotation'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    payment_date = fields.Datetime(string='Payment Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now)

