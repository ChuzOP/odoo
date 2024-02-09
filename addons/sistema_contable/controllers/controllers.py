# -*- coding: utf-8 -*-
# from odoo import http


# class SistemaContable(http.Controller):
#     @http.route('/sistema_contable/sistema_contable', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sistema_contable/sistema_contable/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sistema_contable.listing', {
#             'root': '/sistema_contable/sistema_contable',
#             'objects': http.request.env['sistema_contable.sistema_contable'].search([]),
#         })

#     @http.route('/sistema_contable/sistema_contable/objects/<model("sistema_contable.sistema_contable"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sistema_contable.object', {
#             'object': obj
#         })

