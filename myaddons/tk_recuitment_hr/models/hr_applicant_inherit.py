from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError

class Applicant(models.Model):
    _inherit = "hr.applicant"

    employee_id = fields.Many2one(string='Employee introduce',comodel_name='hr.employee',ondelete='restrict',)
    name_source = fields.Char()
    set_criterias_id = fields.Many2one('tk_recruitment_hr.set_criterias','Set critetias',ondelete='restrict',related='job_id.set_criterias_id')
    
    @api.onchange('source_id')
    def _onchange_field(self):
        self.name_source = self.source_id.name
        print(self.name_source)
    
    
    
