# -*- coding: utf-8 -*-
from odoo import http

# class OpBatchFree(http.Controller):
#     @http.route('/op_batch_free/op_batch_free/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/op_batch_free/op_batch_free/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('op_batch_free.listing', {
#             'root': '/op_batch_free/op_batch_free',
#             'objects': http.request.env['op_batch_free.op_batch_free'].search([]),
#         })

#     @http.route('/op_batch_free/op_batch_free/objects/<model("op_batch_free.op_batch_free"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('op_batch_free.object', {
#             'object': obj
#         })