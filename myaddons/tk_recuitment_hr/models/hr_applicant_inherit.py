from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError

class Applicant(models.Model):
    _inherit = "hr.applicant"

    employee_id = fields.Many2one(string='Employee introduce',comodel_name='hr.employee',ondelete='restrict',)
    name_source = fields.Char()
    
    @api.onchange('source_id')
    def _onchange_field(self):
        self.name_source = self.source_id.name
        print(self.name_source)
    
    
    
