# -*- coding: utf-8 -*-

from odoo import api, models, fields

class hs_provinsi(models.Model):
    _name = 'hs.provinsi'
    _order = 'name'

    name = fields.Char('Nama', required=True)
    kabupaten_ids = fields.One2many('hs.kabupaten', 'provinsi_id', string='Data Kabupaten')
    