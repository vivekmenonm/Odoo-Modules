# -*- coding: utf-8 -*-

from odoo import models, fields, api


@api.model
def _get_target_year_list(self):
    year_list = []
    for year in range(2000, 2101):
        year_list.append(('%s' % (year), '%s' % (year)))
    return year_list

@api.model
def _get_target_month_list(self):
    month_list = [
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]
    return month_list
    
    
class ProjectType(models.Model):
    _name = 'project.type'
    _description = 'Project Type'
    
    name = fields.Char('Project Type', required=True)
    code = fields.Char('Code')
    active = fields.Boolean(default=True)
    
    def name_get(self):
        result = []
        for type in self:
            if type.code:
                result.append((type.id, "%s %s" % (type.code, type.name)))
            else:
                result.append((type.id, "%s" % (type.name)))
        return result
    
    
class Project(models.Model):
    _inherit = 'project.project'
    
    productivity = fields.Integer('Records Per Hours')
    project_type_id = fields.Many2one('project.type', 'Project Type')
    target_year = fields.Selection(_get_target_year_list, string='Target Year')
    target_month = fields.Selection(_get_target_month_list, string='Target Month')
    employee_ids = fields.Many2many('hr.employee', 'project_hr_employee_rel', 'project_id', 'employee_id', string='Employees')
    
    @api.model
    def default_get(self, field_list):
        today = fields.Date.today()
        res = super(Project, self).default_get(field_list)
        res.update({
            'target_year': str(today.year),
            'target_month': str(today.month),
        })
        return res
        
    
class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    project_type_id = fields.Many2one('project.type', 'Project Type')
    productivity = fields.Integer('Records Per Hours')
    target_year = fields.Selection(_get_target_year_list, string='Target Year')
    target_month = fields.Selection(_get_target_month_list, string='Target Month')
    project_employee_ids = fields.Many2many('hr.employee', related="project_id.employee_ids", string='Project Employees')
    employee_ids = fields.Many2many('hr.employee', 'project_task_hr_employee_rel', 'project_task_id', 'employee_id', string='Employees', 
                                    domain="[('id', 'in', project_employee_ids)]")
    
            
    @api.model
    def default_get(self, field_list):
        context = self.env.context
        today = fields.Date.today()
        res = super(ProjectTask, self).default_get(field_list)
        res.update({
            'target_year': str(today.year),
            'target_month': str(today.month),
        })
        if 'default_project_id' in context and context['default_project_id']:
            project = self.env['project.project'].browse(context['default_project_id'])
            res.update({
                'project_type_id': project.project_type_id.id,
                'productivity': project.productivity,
            })
        return res
    
    @api.onchange('project_id')
    def _change_project_productivity(self):
        if self.project_id:
            self.update({
                'project_type_id': self.project_id.project_type_id.id,
                'productivity': self.project_id.productivity
            })
    
    