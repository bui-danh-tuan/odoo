from odoo import models, fields, api

class criteria_category(models.Model):
    _name = "hr.recruitment.criteria_category"

    name = fields.Char('Tiêu đề',required=True)

    description = fields.Char('Mô tả chi tiết',)

    category_line_ids = fields.One2many('hr.recruitment.criteria_category_line','criteria_category_id',string='',required=True)

    knowledge_category_line_ids = fields.One2many('hr.recruitment.criteria_category_line','criteria_category_id', string='review', domain=[('type','=','knowledge')])
    skill_category_line_ids = fields.One2many('hr.recruitment.criteria_category_line','criteria_category_id', string='review', domain=[('type','=','skill')])
    spirit_category_line_ids = fields.One2many('hr.recruitment.criteria_category_line','criteria_category_id', string='review', domain=[('type','=','spirit')])


class criteria_category_line(models.Model):
    _name = "hr.recruitment.criteria_category_line"
    
    criteria_category_id = fields.Many2one('hr.recruitment.criteria_category','criteria_category',ondelete='cascade')

    criteria_id = fields.Many2one('hr.recruitment.criteria','Tiêu chí đánh giá',ondelete='cascade',required=True)

    rating_weight = fields.Integer('Trọng số đánh giá',)

    description = fields.Char('Mô tả chi tiết')
    
    description_ = fields.Text('Mô tả tiêu chí',related='criteria_id.description')
    
    type = fields.Selection(selection=[
    ('knowledge', 'kiến Thức'), 
    ('skill','Kĩ năng/ kinh nhiệm'), 
    ('spirit','Thái độ')],
    related='criteria_id.type')
    

    