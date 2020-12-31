# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime, timedelta 
import pytz

class op_repuest_join_batch(models.Model):
    _name = 'op.request.join.batch'

    state =  fields.Selection([('new', 'New'),('approve', 'Approve'),('cancel', 'Cancel'),],'Trạng thái',default='new')
    
    name = fields.Char('Tên buổi học')
    batch_free_id = fields.Many2one('op.batch.free','Buổi học')

    partner_id = fields.Many2one('res.partner','Người đăng kí')
    
    repuest_datetime = fields.Datetime('Thời gian đăng ký', default=datetime.now())
    start_datetime = fields.Datetime('Thời gian bắt đầu', related='batch_free_id.start_datetime')
    end_datetime = fields.Datetime('Thời gian kết thúc', related='batch_free_id.end_datetime')
    duration_datetime = fields.Integer('Thời lượng buổi học (phút)', related='batch_free_id.duration_datetime')
    
    student_max = fields.Integer('Số học viên tối đa', related='batch_free_id.student_max')
    faculty_id = fields.Many2one(related='batch_free_id.faculty_id')
    course_id = fields.Many2one(related='batch_free_id.course_id')
    link_batch = fields.Char('Link buổi học', related='batch_free_id.link_batch')
    
    description = fields.Text('Ghi chú')
    

    @api.onchange('partner_id','batch_free_id')
    def get_name_of_batch(self):
        if self.partner_id and self.batch_free_id:
            self.name = str(self.partner_id.name) + ' - ' + str(self.course_id.name) + ' - '  + str(self.start_datetime)
            print(self.name)

    @api.multi
    def action_approve(self):
        self.state = 'approve'

    @api.multi
    def action_cancel(self):
        self.state = 'cancel'

