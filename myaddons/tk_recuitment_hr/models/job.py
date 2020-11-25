from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError

class job(models.Model):
    _name = "tk_recuitment_hr.job"
    _inherit = ['mail.thread']

    name                = fields.Char(string="Tên vị trí",required = True,)
    department_id       = fields.Many2one('hr.department','Phòng ban',required = True,)
    company_id          = fields.Many2one('res.company','Công ty',required = True,)
    description         = fields.Text(string="Mô tả",)
    set_criterias_id    = fields.Many2one('tk_recruitment_hr.set_criterias','Bộ tiêu chí',ondelete='restrict',required = True,)
    created_at          = fields.Date(string='Ngày tạo',default=fields.Date.context_today,readonly=True,required=True)
    create_uid          = fields.Many2one('res.users','Người tạo', default=lambda self: self.env.user, readonly=True)
    state               = fields.Selection([('draft', 'Biên soạn'), ('submit', 'Chờ duyệt'), ('approved', 'Đã duyệt'),('cancel','Không được duyệt')],default='draft')

    @api.onchange('company_id')
    def _onchange_company_id(self):
        self.department_id = ''

    @api.onchange('name','department_id','company_id')
    def _check_duplicate_job(self):
        if(self.name and self.department_id and self.company_id):
            job_position = self.env['hr.job'].search([
                ('name', '=', self.name), 
                ('company_id', '=', self.company_id.id),
                ('department_id','=',self.department_id.id)])
            tk_job_position = self.env['tk_recuitment_hr.job'].search([
                ('name', '=', self.name), 
                ('company_id', '=', self.company_id.id),
                ('department_id','=',self.department_id.id)])
            if job_position or tk_job_position:
                self.name = None
                self.company_id = None
                self.department_id = None
                return {
                    'warning': {
                    'title': _('Lỗi trùng lặp!'),
                    'message': _('Vị trí bạn muốn thêm đã tồn tại!'),
                }}

    @api.multi
    def submit(self):
        self.state = 'submit'

    @api.multi
    def cancel(self):
        self.state = 'cancel'

    @api.multi
    def draft(self):
        self.state = 'draft'

    @api.multi
    def uncancel(self):
        self.state = 'draft'

    @api.multi
    def approved(self):
        self.env ['hr.job']. create ({
            'name':self.name,
            'description': self.description,
            'department_id': self.department_id.id,
            'company_id': self.company_id.id,
            'state': 'recruit',
            'set_criterias_id':self.set_criterias_id.id,
            'created_at':self.created_at,
            'create_uid':self.create_uid
        })
        self.state='approved'
