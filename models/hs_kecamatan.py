# -*- coding: utf-8 -*-

from odoo import api, models, fields

class hs_kecamatan(models.Model):
    _name = 'hs.kecamatan'
    _order = 'name'
    
    name = fields.Char('Nama', required=True)
    kabupaten_id = fields.Many2one('hs.kabupaten', 'Kabupaten')
