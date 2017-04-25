from odoo import api, models, fields 

class hs_karyawan(models.Model):
	_name = 'hs.karyawan'

	kode = fields.Char('Kode')
	# Daftar field
	name = fields.Char('Nama', required=True)
	panggilan = fields.Char('Panggilan')
	aktif = fields.Boolean("Aktif", default=True, required=True)
	telp = fields.Char('Telp')
	ktp = fields.Char('KTP')
	tempat_lahir = fields.Char('Tempat Lahir')
	tgl_lahir = fields.Date('Tanggal Lahir')
	alamat = fields.Char('Alamat')
	provinsi_id = fields.Many2one('hs.provinsi', 'Provinsi')
	kabupaten_id = fields.Many2one('hs.kabupaten', 'Kabupaten')
	kecamatan_id = fields.Many2one('hs.kecamatan', 'Kecamatan')
	jabatan = fields.Selection([('DRV', 'DRIVER'), ('STF', 'STAFF')], required=True)
	gaji_per_shift = fields.Float('Gaji per Shift')
	armada_id = fields.Many2one('hs.armada', domain=lambda self: [('id', 'not in', self._get_armada_ids())], string='Armada')

	@api.multi
	def _get_armada_ids(self):
		karyawan_ids = self.env['hs.karyawan'].search([('armada_id', '!=', '')])
		armada_ids = []
		for kary in karyawan_ids:
			armada_ids.append(kary.armada_id.id)
		return armada_ids

	@api.model
	def create(self, vals):
		# Generate Kode
		#### Get jenis jabatan
		jabatan = vals['jabatan']
		if jabatan:
			prefix = ""
			counter = 0
			if jabatan == 'STF':
				prefix = self.env['hs.appkonfig'].search([('name','=','staff_kode_prefix')])
				counter = self.env['hs.appkonfig'].search([('name','=','staff_kode_counter')])
			elif jabatan == 'DRV':
				prefix = self.env['hs.appkonfig'].search([('name','=','driver_kode_prefix')])
				counter = self.env['hs.appkonfig'].search([('name','=','driver_kode_counter')])
			# Generate Kode
			kode = prefix[0].value + counter[0].value            
			# update kode
			vals.update({'kode':kode})        
		# insert new data
		print('call super method')
		newrow = super(hs_karyawan,self).create(vals)
		print('Create new karyawan done')
		# Update counter
		if jabatan:
			new_counter = int(counter[0].value)+1
			counter.write({'value':new_counter})   

		return newrow


	@api.multi
	def write(self, vals):
		if vals.get('jabatan',False):
			jabatan = vals['jabatan']
			prefix = ""
			counter = 0
			if jabatan == 'STF':
				prefix = self.env['hs.appkonfig'].search([('name','=','staff_kode_prefix')])
				counter = self.env['hs.appkonfig'].search([('name','=','staff_kode_counter')])
			elif jabatan == 'DRV':
				prefix = self.env['hs.appkonfig'].search([('name','=','driver_kode_prefix')])
				counter = self.env['hs.appkonfig'].search([('name','=','driver_kode_counter')])
			# Generate Kode
			kode = prefix[0].value + counter[0].value            
			# update kode
			vals.update({'kode':kode})     
			# update counter
			new_counter = int(counter[0].value)+1
			counter.write({'value':new_counter})  
		return super(hs_karyawan,self).write(vals)


	# @api.multi
	# def name_get(self,cr,uid,ids,context=None):
	# 	result = {}
	# 	for partner in self.browse(cr,uid,ids,context=context):
	# 		result[partner.id] = partner.name + " " + partner.kode

	# 	return result.items()
	# @api.multi
	# def _display_name(self):
	# 	result = {}
	# 	for partner in self:
	# 		result[partner.id] = partner.name + "-" + partner.name
	
	# 	return result.items()

	# @api.one
	# def display_name(self,cr,uid,ids,context=None):
	# 	if context is None:
	# 		context ={}
	# 	res=[]
	# 	record_name=self.browse(cr,uid,ids,context)
	# 	for partner in record_name:
	# 		result[partner.id] = partner.name + " " + partner.kode
		
	# 	return res

	# override untuk menampiklkan 2 colum dalam satu selection
	@api.multi
	def name_get(self, context=False):
		# if context is None:
		# 	context ={}
		res=[]
		# record_name=self.search()
		# print(context.get('show_kode',False))
		# print(context)

		for object in self:
			# if object.name:
				# if context.get('show_kode',False):
					#name for contact_address_id field
			res.append((object.id,str(object.armada_id.name)+" - "+str(object.name)))
				# else:
					#name for contact_id field
					# res.append((object.id,object.name))
		return res

	# Override untuk searching berdasarkan nama dan armada
	@api.model
	def name_search(self, name, args=None, operator='ilike', limit=100):
		args = args or []
		recs = self.browse()
		if name:
			recs = self.search((args + ['|', ('name', 'ilike', name), ('armada_id', 'ilike', name)]),
                               limit=limit)
		if not recs:
			recs = self.search([('name', operator, name)] + args, limit=limit)

		return recs.name_get()