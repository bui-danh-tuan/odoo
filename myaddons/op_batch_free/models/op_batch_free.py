# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime, timedelta 
import pytz
from odoo.exceptions import UserError

class op_batch_free(models.Model):
    _name = 'op.batch.free'

    state =  fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'), ('cancel', 'Cancel')],'Trạng thái',default='draft')
    
    name = fields.Char('Tên buổi học')
    description = fields.Text('Giới thiệu về buổi học')

    request_count = fields.Integer(string='Student Request', compute='get_request')
    
    course_id = fields.Many2one('op.course','Môn học')
    student_max = fields.Integer('Số học viên tối đa')
    faculty_id = fields.Many2one('op.faculty','Giảng viên')
    start_datetime = fields.Datetime('Thời gian bắt đầu')
    end_datetime = fields.Datetime('Thời gian kết thúc')
    duration_datetime = fields.Integer('Thời lượng buổi học (phút)', compute='get_duration_datetime' )

    partner_ids = fields.Many2many('res.partner', string='Học viên đã đăng kí', compute='get_request' )
    link_batch = fields.Char('Link buổi học')

    repuest_join_batch_ids = fields.One2many(string='Tất cả yêu cầu',comodel_name='op.request.join.batch',inverse_name='batch_free_id',)

    @api.depends('start_datetime','end_datetime')
    def get_duration_datetime(self):
        if self.start_datetime and self.end_datetime:
            st_dt = fields.Datetime.from_string(self.start_datetime)
            en_dt = fields.Datetime.from_string(self.end_datetime)

            duration_datetime = en_dt - st_dt
            duration_datetime = duration_datetime.seconds//60
            self.duration_datetime = int(duration_datetime)

    @api.depends('repuest_join_batch_ids')
    def get_request(self):
        self.request_count = len(self.repuest_join_batch_ids)
        values  = []
        for rq in self.repuest_join_batch_ids:
            if rq.state == 'approve':
                values.append((4,rq.partner_id.id,0))
        self.update({
            'partner_ids':values
        })
        print(self.partner_ids)

    @api.onchange('start_datetime')
    def _onchange_start_datetime(self):
        if self.start_datetime:
            self.end_datetime = self.start_datetime
    
    # @api.multi
    # def write(self, vals):
    #     res = super(op_batch_free, self).write(vals)
    #     minute_now = 0
    #     minute_end = 0
    #     user_tz = self.env.user.tz or str(pytz.utc)
    #     tz_now = datetime.now(pytz.timezone(user_tz))
    #     diff = int(tz_now.utcoffset().total_seconds() / 60 / 60)

    #     st_dt = fields.Datetime.from_string(self.start_datetime) + timedelta(hours=diff)
    #     en_dt = fields.Datetime.from_string(self.end_datetime) + timedelta(hours=diff)
    #     now = datetime.now()

    #     if st_dt > now:
    #         delta_datetime_now = st_dt - now
    #         minute_now = int(delta_datetime_now.seconds//60)
    #         if st_dt < en_dt:
    #             delta_datetime_end = st_dt - en_dt
    #             minute_end = int(delta_datetime_now.seconds//60)

            
    #     if minute_now < 120:
    #         raise UserError(_('Thời gian bắt đầu cần lớn hơn thời gian hiện tại ít nhất 120p!'))
    #     elif minute_end < 30:
    #         raise UserError(_('Thời gian bắt đầu cần lớn hơn thời gian kết thúc ít nhât 30p!'))
    #     else:
    #         return res

    @api.onchange('end_datetime')
    def _onchange_end_datetime(self):
        if self.start_datetime and self.end_datetime:
            user_tz = self.env.user.tz or str(pytz.utc)
            tz_now = datetime.now(pytz.timezone(user_tz))
            diff = int(tz_now.utcoffset().total_seconds() / 60 / 60)

            st_dt = fields.Datetime.from_string(self.start_datetime) + timedelta(hours=diff)
            en_dt = fields.Datetime.from_string(self.end_datetime) + timedelta(hours=diff)
            st_date = fields.Date.from_string(str(st_dt))
            en_date = fields.Date.from_string(str(en_dt))

            if st_date!=en_date:
                self.end_datetime = self.start_datetime
                return {
                    'warning': {
                    'title': _('Thông báo lỗi!'),
                    'message': _('Thời gian bắt đầu và kết thúc phải trong cùng 1 ngày!'),
                }}
            elif en_dt < st_dt:
                self.end_datetime = self.start_datetime
                return {
                    'warning': {
                    'title': _('Thông báo lỗi!'),
                    'message': _('Thời gian kết thúc phải sau thời gian bắt đầu ít nhât 30 phút!'),
                }}
    
    @api.multi
    def action_create_request(self):
        action = self.env.ref('op_batch_free.action_op_request_join_batch').read()[0]
        action['domain'] = [('batch_free_id','in', self.ids)]
        action['context'] = {'default_batch_free_id': self.id,}
        return action

    @api.multi
    def action_confirm(self):
        self.state = 'confirm'

    @api.multi
    def action_done(self):
        user_tz = self.env.user.tz or str(pytz.utc)
        tz_now = datetime.now(pytz.timezone(user_tz))
        diff = int(tz_now.utcoffset().total_seconds() / 60 / 60)

        en_dt = fields.Datetime.from_string(self.end_datetime) + timedelta(hours=diff)
        now = datetime.now()
        if self.state == 'confirm' and now  > en_dt:
            self.state = 'done'
        elif now < en_dt:
            raise UserError(_('Do lớp học chưa kết thúc nên chưa thể xét trạng thái là done. Vui lòng đợi lớp học kết thúc lúc{}!'.format(self.start_datetime)))

    @api.multi
    def action_cancel(self):
        user_tz = self.env.user.tz or str(pytz.utc)
        tz_now = datetime.now(pytz.timezone(user_tz))
        diff = int(tz_now.utcoffset().total_seconds() / 60 / 60)

        st_dt = fields.Datetime.from_string(self.start_datetime) + timedelta(hours=diff)
        now = datetime.now()
        delta_datetime_now = st_dt - now
        minute_now = int(delta_datetime_now.seconds//60)
        if minute_now <=15 and len(self.partner_ids) <= 0:
            self.state = 'cancel'
        elif len(self.partner_ids) > 0:
            raise UserError(_('Do lớp học đã có học sinh đăng kí nên không thể  hủy!'))
        elif minute_now > 15:
            raise UserError(_('Lớp học chỉ có thể hủy khi đã đến 15 phút trước buổi học mà không có học sinh nào đăng kí.'))
    
    def cron_auto_done_batch_free(self):
        user_tz = self.env.user.tz or str(pytz.utc)
        tz_now = datetime.now(pytz.timezone(user_tz))
        diff = int(tz_now.utcoffset().total_seconds() / 60 / 60)

        en_dt = fields.Datetime.from_string(self.end_datetime) + timedelta(hours=diff)
        now = datetime.now()
        if self.state == 'confirm' and now  > en_dt:
            self.state = 'done'
