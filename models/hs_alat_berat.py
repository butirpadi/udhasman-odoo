from odoo import api, models, fields

class hs_alat_berat(models.Model):
	_name = "hs.alat.berat"

	name = fields.Char('Nama')
	kode = fields.Char('Kode')
	# keterangan = fields.Char('Nama')

	# @api.model 
	# def create(self,vals):
	# 	# set name
	# 	vals['name'] = vals['kode'] + ' - ' + vals['keterangan']
	# 	return super(hs_alat_berat,self).create(vals)

	# @api.model 
	# def write(self,vals):
	# 	# set name
	# 	kode = ''
	# 	if vals.has_key('kode'):
	# 		kode  = vals['kode']
	# 	else
	# 		kode = self.kode

	# 	keterangan = ''
	# 	if vals.has_key('keterangan'):
	# 		keterangan  = vals['keterangan']
	# 	else
	# 		keterangan = self.keterangan

	# 	vals['name'] = kode + ' - ' + keterangan
	# 	return super(hs_alat_berat,self).write(vals)
