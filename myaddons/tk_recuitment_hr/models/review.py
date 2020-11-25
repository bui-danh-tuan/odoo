from odoo import models, fields, api

class review(models.Model):
    
    _name = "tk_recruitment_hr.review"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char('Bản đánh giá',default='Bản đánh giá')
    
    type                = fields.Selection(selection=[('R', 'Recruitment'), ('H', 'Human Resources')],required = True)
    order               = fields.Integer(default=0)
    active              = fields.Boolean(default=True)
    description         = fields.Text()
    set_criterias_id    = fields.Many2one('tk_recruitment_hr.set_criterias','set criterias',ondelete='restrict',)
    reivew_line_ids     = fields.One2many('tk_recruitment_hr.review_line','review_id','reivew_line',)
    # applicant_id        = fields.Many2one(string='CV đánh giá',comodel_name='hr.applicant',ondelete='restrict',)
    total_score         = fields.Float(default=0,compute='_get_total')
    average_score       = fields.Float(default=0,compute='_get_average')
    created_at          = fields.Date(string='Ngày đánh giá',default=fields.Date.context_today,readonly=True,required=True)
    create_uid          = fields.Many2one('res.users','Người đánh giá', default=lambda self: self.env.user, readonly=True)

    # applicant_company   = fields.Many2one(related='applicant_id.company_id',)
    # applicant_department= fields.Many2one(related='applicant_id.department_id',)
    # applicant_job       = fields.Many2one(related='applicant_id.job_id',)
    # applicant_mobile    = fields.Char(related='applicant_id.partner_mobile',)
    # applicant_partner_name = fields.Char(related='applicant_id.partner_name',)
    
    @api.onchange('set_criterias_id')
    def _onchange_set_criterias_id(self):
        self.update({
                'reivew_line_ids' : [(2,s.id,0) for s in self.reivew_line_ids]
            })
        if self.set_criterias_id:
            all_criterias = self.set_criterias_id.criterias_line_ids
            self.update({
                'reivew_line_ids' : [(0,0,{
                    'criterias_id':s.criterias_id.id,
                    'rating_weight':s.rating_weight,
                    'description':s.description,
                    'group_criterias_id':s.group_criterias_id.id
                }) for s in all_criterias]
            })
    
    @api.depends('reivew_line_ids')
    def _get_total(self):
        total_score_ = 0
        for category in self.reivew_line_ids:
            total_score_ += float(category.total_score)
        self.update({'total_score':total_score_})

    @api.depends('reivew_line_ids')
    def _get_average(self):
        total_score_ = 0
        count_ = 0
        average_score_ = 0
        for category in self.reivew_line_ids:
            total_score_ += float(category.total_score)
            count_ += 1
        if count_ > 0:
            average_score_ = float(total_score_ / count_)
        self.update({'average_score':average_score_})

    @api.multi
    def action_print_pdf(self):
        return self.env.ref('tk_recruitment_hr.action_report_review').report_action(self)
    
class review_line(models.Model):
    _name = 'tk_recruitment_hr.review_line'

    criterias_id    =   fields.Many2one('tk_recruitment_hr.criterias','criterias_id',ondelete='CASCADE',)
    review_id       =   fields.Many2one('tk_recruitment_hr.review','review_id',ondelete='CASCADE',)
    rating_weight   =   fields.Integer()
    score           =   fields.Integer()
    total_score     =   fields.Integer(compute='_get_total')
    description     =   fields.Text()
    group_criterias_id =   fields.Many2one(comodel_name='tk_recruitment_hr.group_criterias',ondelete='restrict')
    
    @api.depends('score')
    def _get_total(self):
        for rec in self:
           rec.update({
                'total_score' : rec.score*rec.rating_weight,
            })