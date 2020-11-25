# -*- coding: utf-8 -*-

from odoo import models, fields, api

class criteria(models.Model):
    _name = "hr.recruitment.criteria"

    name = fields.Char('Tên',required=True)
    
    type = fields.Selection(selection=[('knowledge', 'kiến Thức'), ('skill','Kĩ năng/ kinh nhiệm'), ('spirit','Thái độ')],required=True)

    description = fields.Text('Mô tả chi tiết')
    
    
    