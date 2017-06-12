from odoo import api, models, fields

class hs_appkonfig(models.Model):
    _name = 'hs.appkonfig'
    _description = 'Application Config Data'

    name = fields.Char('Name', required=True)
    desc = fields.Char('Nama')
    value = fields.Text('Value')