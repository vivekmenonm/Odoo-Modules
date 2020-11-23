# -*- coding: utf-8 -*-

from odoo import models, fields, api
    
    
class CRMLead(models.Model):
    _inherit = 'crm.lead'
    
    approx_bill = fields.Char('Approximate Billing')
    record_count = fields.Integer('Record Count')
    department = fields.Char('Department')
    sample_done_employee_id = fields.Many2one('hr.employee', 'Sample done by')
    sample_status = fields.Selection([('waiting', 'Waiting for sample'), ('progress', 'Sample in progress'), ('client_response', 'Waiting Client Response')], \
                                     string="Sample Status")
    sample_priority = fields.Selection([('p1', 'Priority 1'), ('p2', 'Priority 2'), ('p3', 'Priority 3'), ('p4', 'Priority 4')], \
                                     string="Sample Priority")
    
    