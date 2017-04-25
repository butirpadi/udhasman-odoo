# -*- coding: utf-8 -*-
from odoo import http

# class Udhasman(http.Controller):
#     @http.route('/udhasman/udhasman/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/udhasman/udhasman/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('udhasman.listing', {
#             'root': '/udhasman/udhasman',
#             'objects': http.request.env['udhasman.udhasman'].search([]),
#         })

#     @http.route('/udhasman/udhasman/objects/<model("udhasman.udhasman"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('udhasman.object', {
#             'object': obj
#         })