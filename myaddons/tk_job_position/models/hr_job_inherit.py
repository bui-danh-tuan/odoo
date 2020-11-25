from odoo import models, fields, api

class job_inherit(models.Model):
    _inherit = "hr.job"

    set_criterias_id    = fields.Many2one('tk_recruitment_hr.set_criterias','Bộ tiêu chí',ondelete='restrict',)
    created_at          = fields.Date(string='Ngày tạo',default=fields.Date.context_today,readonly=True,required=True)
    create_uid          = fields.Many2one('res.users','Người tạo', default=lambda self: self.env.user, readonly=True)