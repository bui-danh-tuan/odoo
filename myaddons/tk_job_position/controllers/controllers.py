# -*- coding: utf-8 -*-
from odoo import http

# class TkJobPosition(http.Controller):
#     @http.route('/tk_job_position/tk_job_position/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tk_job_position/tk_job_position/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tk_job_position.listing', {
#             'root': '/tk_job_position/tk_job_position',
#             'objects': http.request.env['tk_job_position.tk_job_position'].search([]),
#         })

#     @http.route('/tk_job_position/tk_job_position/objects/<model("tk_job_position.tk_job_position"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tk_job_position.object', {
#             'object': obj
#         })