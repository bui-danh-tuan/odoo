# -*- coding: utf-8 -*-
from odoo import http

# class TkRecuitmentHr(http.Controller):
#     @http.route('/tk_recuitment_hr/tk_recuitment_hr/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tk_recuitment_hr/tk_recuitment_hr/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tk_recuitment_hr.listing', {
#             'root': '/tk_recuitment_hr/tk_recuitment_hr',
#             'objects': http.request.env['tk_recuitment_hr.tk_recuitment_hr'].search([]),
#         })

#     @http.route('/tk_recuitment_hr/tk_recuitment_hr/objects/<model("tk_recuitment_hr.tk_recuitment_hr"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tk_recuitment_hr.object', {
#             'object': obj
#         })