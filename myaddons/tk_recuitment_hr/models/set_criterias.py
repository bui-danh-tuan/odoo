from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError, ValidationError

class set_criterias(models.Model):
    
    _name = "tk_recruitment_hr.set_criterias"
    _inherit = ['mail.thread','mail.activity.mixin']

    name        = fields.Char(required = True,default="")
    type        = fields.Selection(selection=[('R', 'Recruitment'), ('H', 'Human Resources')],required = True, default='R')
    order       = fields.Integer(default=0)
    active      = fields.Boolean(default=True)
    description = fields.Text()

    group_criterias_line_ids = fields.Many2many('tk_recruitment_hr.group_criterias','set_group_rel','set_criterias_ids','group_criterias_id',string='group_criterias',required = True)
    criterias_line_ids = fields.One2many('tk_recruitment_hr.criterias_line','set_criterias_id',string='criterias_line_ids',required = True)
    job_line_ids = fields.Many2many('hr.job','set_criterias_job_rel','set_criterias_id','job_id',string='job_line_ids',required = True)
    criterias_ids = fields.Many2many('tk_recruitment_hr.criterias',compute='_get_criterias_ids')
    

    @api.depends('criterias_line_ids')
    def _get_criterias_ids(self):
        for s in self:
            s.criterias_ids = [i.criterias_id.id for i in s.criterias_line_ids]

    # @api.onchange('criterias_line_ids')
    # @api.constrains('criterias_line_ids')
    # def _check_criterias(self):
    #     n = len(self.criterias_line_ids)
    #     if n > 0:
    #         for i in range(0,n-1):
    #             if(self.criterias_line_ids[i].criterias_id==self.criterias_line_ids[-1].criterias_id):
    #                 raise ValidationError("\""+self.criterias_line_ids[i].criterias_id.name+"\""+' bi trung')
    
    @api.onchange('group_criterias_line_ids')
    def _check_delete_group(self):
        for criterias in self.criterias_line_ids:
            check = False
            for group in self.group_criterias_line_ids:
                if criterias.group_criterias_id == group:
                    check = True
                    break
            if check == False:
                self.criterias_line_ids = [(2,criterias.id,0)]
                
class criterias_line(models.Model):

    _name = "tk_recruitment_hr.criterias_line"

    criterias_id = fields.Many2one('tk_recruitment_hr.criterias','criterias_id',ondelete='CASCADE',required = True)
    set_criterias_id = fields.Many2one('tk_recruitment_hr.set_criterias','set_criterias_id',ondelete='CASCADE',)
    group_criterias_id  = fields.Many2one('tk_recruitment_hr.group_criterias','group_criterias_id',ondelete='restrict',related='criterias_id.group_criterias_id')

    rating_weight = fields.Integer(default=0,required = True)
    description = fields.Text(related='criterias_id.description')

class job_inherit(models.Model):
    _inherit = "hr.job"
    set_criterias_ids = fields.Many2many('tk_recruitment_hr.set_criterias','set_criterias_job_rel','job_id','set_criterias_id',string='job_line_ids')

