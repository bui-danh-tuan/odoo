from odoo import models, fields, api
from datetime import datetime
class group_criterias(models.Model):
    
    _name = "tk_recruitment_hr.group_criterias"
    _inherit = ['mail.thread']

    name        = fields.Char(required = True, default="")
    description = fields.Text()
    active      = fields.Boolean(default=True)
    type        = fields.Selection(selection=[('R', 'Recruitment'), ('H', 'Human Resources')],required = True,default='R')
    order       = fields.Integer(default=0)

    set_criterias_ids = fields.Many2many('tk_recruitment_hr.set_criterias','set_group_rel','group_criterias_id','set_criterias_ids',string='set_criterias',)
    
    