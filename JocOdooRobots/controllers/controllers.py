# -*- coding: utf-8 -*-
# from odoo import http


# class Joc(http.Controller):
#     @http.route('/joc/joc', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/joc/joc/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('joc.listing', {
#             'root': '/joc/joc',
#             'objects': http.request.env['joc.joc'].search([]),
#         })

#     @http.route('/joc/joc/objects/<model("joc.joc"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('joc.object', {
#             'object': obj
#         })
