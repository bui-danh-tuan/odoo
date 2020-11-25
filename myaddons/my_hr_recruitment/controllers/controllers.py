# -*- coding: utf-8 -*-
from odoo import http

# class MyHrRecruitment(http.Controller):
#     @http.route('/my_hr_recruitment/my_hr_recruitment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_hr_recruitment/my_hr_recruitment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_hr_recruitment.listing', {
#             'root': '/my_hr_recruitment/my_hr_recruitment',
#             'objects': http.request.env['my_hr_recruitment.my_hr_recruitment'].search([]),
#         })

#     @http.route('/my_hr_recruitment/my_hr_recruitment/objects/<model("my_hr_recruitment.my_hr_recruitment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_hr_recruitment.object', {
#             'object': obj
#         })