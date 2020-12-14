from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class Applicant(models.Model):
    _inherit = "hr.applicant"

    employee_id = fields.Many2one(
        string='Employee introduce', comodel_name='hr.employee', ondelete='restrict',)
    name_source = fields.Char()
    set_criterias_id = fields.Many2one('tk_recruitment_hr.set_criterias',
                                       'Set critetias', ondelete='restrict', related='job_id.set_criterias_id')
    name_stage = fields.Char(related="stage_id.name")

    @api.onchange('source_id')
    def _onchange_field(self):
        self.name_source = self.source_id.name
        print(self.name_source)

    order = fields.Integer(default=0)
    description = fields.Text()
    set_criterias_id = fields.Many2one(
        'tk_recruitment_hr.set_criterias', 'set criterias', ondelete='restrict',)
    reivew_line_ids = fields.One2many(
        'tk_recruitment_hr.review_line_', 'review_id', 'reivew_line',)
    total_score = fields.Float(default=0, compute='_get_total')
    average_score = fields.Float(default=0, compute='_get_average')
    created_at = fields.Date(
        string='Ngày đánh giá', default=fields.Date.context_today, readonly=True, required=True)
    create_uid = fields.Many2one(
        'res.users', 'Người đánh giá', default=lambda self: self.env.user, readonly=True)

    @api.onchange('set_criterias_id',)
    def _onchange_set_criterias_id(self):
        self.update({
            'reivew_line_ids': [(2, s.id, 0) for s in self.reivew_line_ids]
        })
        if self.set_criterias_id:
            all_criterias = self.set_criterias_id.criterias_line_ids
            self.update({
                'reivew_line_ids': [(0, 0, {
                    'criterias_id': s.criterias_id.id,
                    'rating_weight': s.rating_weight,
                    'description': s.description,
                    'group_criterias_id': s.group_criterias_id.id
                }) for s in all_criterias]
            })

    @api.depends('reivew_line_ids')
    def _get_total(self):
        total_score_ = 0
        for category in self.reivew_line_ids:
            total_score_ += float(category.total_score)
        self.update({'total_score': total_score_})

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
        self.update({'average_score': average_score_})

    @api.onchange('name_stage')
    def _onchange_set_criterias_id(self):
        if self.set_criterias_id and self.set_criterias_id.criterias_line_ids == None:
            all_criterias = self.set_criterias_id.criterias_line_ids
            self.update({
                'reivew_line_ids': [(0, 0, {
                    'criterias_id': s.criterias_id.id,
                    'rating_weight': s.rating_weight,
                    'description': s.description,
                    'group_criterias_id': s.group_criterias_id.id
                }) for s in all_criterias]
            })

    @api.multi
    def action_send_mail(self):
        template_id = self.env.ref(
            'tk_recuitment_hr.mail_template_interview_results', raise_if_not_found=False).id
        compose_form = self.env.ref(
            'mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='hr.applicant',
            default_res_id=self.id,
            default_composition_mode='comment',
            default_use_teamplate=True,
            default_template_id=template_id,
            mark_invoice_as_sent=True,
            force_email=True,
        )
        return {
            'name': _('Thông báo training'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    @api.multi
    def action_print_pdf(self):
        return self.env.ref('tk_recuitment_hr.action_review').report_action(self)


class review_line_(models.Model):
    _name = 'tk_recruitment_hr.review_line_'

    criterias_id = fields.Many2one(
        'tk_recruitment_hr.criterias', 'criterias_id', ondelete='CASCADE',)
    review_id = fields.Many2one(
        'hr.applicant', 'review_id', ondelete='CASCADE',)
    rating_weight = fields.Integer()
    score = fields.Integer()
    total_score = fields.Integer(compute='_get_total')
    description = fields.Text()
    group_criterias_id = fields.Many2one(
        comodel_name='tk_recruitment_hr.group_criterias', ondelete='restrict')

    @api.depends('score')
    def _get_total(self):
        for rec in self:
            rec.update({
                'total_score': rec.score*rec.rating_weight,
            })
