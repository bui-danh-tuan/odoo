from odoo import models, fields, api

class criterias(models.Model):
    
    _name = "tk_recruitment_hr.criterias"
    _inherit = ['mail.thread']

    group_criterias_id  = fields.Many2one(comodel_name='tk_recruitment_hr.group_criterias',ondelete='restrict')
    
    name        = fields.Char(required=True,default="")
    description = fields.Text()
    order       = fields.Integer(default=0)
    active  = fields.Boolean(default=True)

    # active  = fields.Boolean(default=True,compute='_get_active',store=True)
    # active_group = fields.Boolean(related="group_criterias_id.active")
    # active_ = fields.Boolean(default=True)

    # @api.depends('active_group','active_')
    # def _get_active(self):
    #     for s in self:
    #         s.active = s.active_group*s.active_
    
