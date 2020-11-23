# -*- encoding: utf-8 -*-

from odoo import api, fields, models

from datetime import timedelta


class ProductivityReportWizard(models.TransientModel):
    _name = "productivity.report.wizard"
    _description = "Productivity Report Wizard"

    date_from = fields.Date(string='Start Date', required=True)
    date_to = fields.Date(string='End Date', required=True)
    project_ids = fields.Many2many('project.project', 'productivity_report_project_rel', 'productivity_report_id', 'project_id', string="Projects")
    employee_ids = fields.Many2many('hr.employee', 'productivity_report_hr_employee_rel', 'productivity_report_id', 'employee_id', string="Employees")
    

    @api.model
    def default_get(self, field_list):
        today = fields.Date.today()
        res = super(ProductivityReportWizard, self).default_get(field_list)
        res.update({
            'date_from': today.replace(day=1),
            'date_to': today.replace(day=1, month=today.month+1) - timedelta(days=1),
        })
        return res

    def print_productivity_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'project_ids', 'employee_ids'])[0]
        for field in data['form'].keys():
            if isinstance(data['form'][field], tuple):
                data['form'][field] = data['form'][field][0]
        return self.env.ref('custom_project.action_report_productivity_report').report_action(self, data=data)
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: