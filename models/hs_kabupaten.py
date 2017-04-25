# -*- coding: utf-8 -*-

from odoo import api, models, fields

class hs_kabupaten(models.Model):
    _name = 'hs.kabupaten'
    _order = 'name'

    name = fields.Char('Nama', required=True)
    kecamatan_ids = fields.One2many('hs.kecamatan', 'kabupaten_id', 'Data Kecamatan')
    provinsi_id = fields.Many2one('hs.provinsi', 'Provinsi')
