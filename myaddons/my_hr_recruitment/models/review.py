from odoo import models, fields, api

class review(models.Model):
    _name = "hr.recruitment.review"

    _inherit = ['mail.thread']

    state = fields.Selection([('review', 'Đang đánh giá'), ('done', 'Đã đánh giá')], default='review',)
    
    manager_id = fields.Many2one('res.users','Người đánh giá', default=lambda self: self.env.user, readonly=True)
    
    creat_date = fields.Date(string='Ngày đánh giá',default=fields.Date.context_today,readonly=True,required=True)
    
    criteria_category_id = fields.Many2one('hr.recruitment.criteria_category','Biểu mẫu đánh giá',ondelete='restrict',required=True, )
    
    review_ids = fields.One2many('hr.recruitment.review_line', 'review_id', string='review', )
    
    knowledge_review_ids = fields.One2many('hr.recruitment.review_line', 'review_id', string='review', domain=[('type','=','knowledge')])
    
    skill_review_ids = fields.One2many('hr.recruitment.review_line', 'review_id', string='review', domain=[('type','=','skill')])
    
    spirit_review_ids = fields.One2many('hr.recruitment.review_line', 'review_id', string='review', domain=[('type','=','spirit')])

    sum_score = fields.Float(compute='_get_sum', string="Tổng điểm")

    avg_score = fields.Float(compute='_get_avg', string="Điểm trung bình")
    
    @api.onchange('criteria_category_id')
    def _onchange_category(self):
        if self.criteria_category_id:
            all_criteria = self.criteria_category_id.category_line_ids 
            types = ['skill','knowledge','spirit']
            obj = [{'{}_review_ids'.format(t): [(0,0,{
                'criteria_id': s.criteria_id.id,
                'rating_weight': s.rating_weight
            })for s in all_criteria if s.criteria_id.type == t]} for t in types]
            for i in obj:
                self.update(i)
        
    
    @api.depends('review_ids')
    def _get_sum(self):
        sum_score_ = 0
        for category in self.review_ids:
            sum_score_ += category.total_score
        self.update({'sum_score':sum_score_})

    @api.depends('review_ids')
    def _get_avg(self):
        sum_score_ = 0
        count_ = 0
        avg_score_ = 0
        for category in self.review_ids:
            sum_score_ += category.total_score
            count_ += 1
        if count_ > 0:
            avg_score_ = sum_score_ / count_
        self.update({'avg_score':avg_score_})
    
    @api.multi
    def action_done_review(self):
        self.update({
            'state':'done',
        })

class review_line(models.Model):
    _name = "hr.recruitment.review_line"

    review_id = fields.Many2one('hr.recruitment.review','review',ondelete='cascade')    
    
    criteria_id = fields.Many2one('hr.recruitment.criteria','Tiêu chí đánh giá',ondelete='cascade')
    
    type = fields.Selection(selection=[
        ('knowledge', 'kiến Thức'), 
        ('skill','Kĩ năng/ kinh nhiệm'), 
        ('spirit','Thái độ')],
        related='criteria_id.type',string="Kiểu tiêu chí")

    scores = fields.Float("Điểm")
    
    rating_weight = fields.Float("Trọng số")

    note =  fields.Char("Ghi chú")

    total_score = fields.Float(compute='_get_total', string="Tổng điểm")
    
    @api.depends('scores', 'rating_weight')
    def _get_total(self):
        for rec in self:
           rec.update({
                'total_score' : rec.scores*rec.rating_weight,
            })
    
    
