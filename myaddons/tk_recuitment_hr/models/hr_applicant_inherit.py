from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError

class Applicant(models.Model):
    _inherit = "hr.applicant"
    
