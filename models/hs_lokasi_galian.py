# -*- coding: utf-8 -*-

from odoo import api, models, fields

class hs_lokasi_galian(models.Model):
    _name = 'hs.lokasi.galian'
    _order = 'name'
    
    name = fields.Char('Nama', required=True)
    alamat = fields.Char('Alamat')
    kecamatan_id = fields.Many2one(
        'hs.kecamatan',
        string='Kecamatan',
    )
    kabupaten_id = fields.Many2one(
        'hs.kabupaten',
        string='Kabupaten',
    )
    provinsi_id = fields.Many2one(
        'hs.provinsi',
        string='Provinsi',
    )
