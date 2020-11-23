# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Timesheet(models.Model):
    _inherit = 'account.analytic.line'
    
    records = fields.Integer('Total Records')
    productivity_grade = fields.Float('Grade')
    grade_label = fields.Char('Grade Label')
    state = fields.Selection([('draft', 'Draft'), ('submit', 'Submitted'), ('cancel', 'Cancelled')], default='draft', string='Status')
    
    
    def _get_grade_label(self, grade):
        label = ''
        if grade < 80:
            label = 'Poor'
        elif grade >= 80 and grade <90:
            label = 'Average'
        elif grade >= 90 and grade < 95:
            label = 'Above Average'
        elif grade >= 95 and grade < 100:
            label = 'Good'
        elif grade >= 100 and grade <= 110:
            label = 'Very Good'
        elif grade > 110:
            label = 'Outstanding'
        
        return label
        
    
    @api.onchange('records', 'unit_amount')
    def _calc_productivity_grade_from_records(self):
        if self.records and self.unit_amount and self.task_id and self.task_id.productivity:
            grade = round(((self.records / self.unit_amount) / self.task_id.productivity) * 100 ,2)
        else:
            grade = 0.0
        label = self._get_grade_label(grade)
        self.update({
            'productivity_grade': grade,
            'grade_label': label,
        })
    
    @api.model
    def create(self, vals):
        res = super(Timesheet, self).create(vals)
        if res.records and res.unit_amount and res.task_id and res.task_id.productivity:
            grade = round(((res.records / res.unit_amount) / res.task_id.productivity) * 100 ,2)
            label = self._get_grade_label(grade)
            res.update({
                'productivity_grade': grade,
                'grade_label': label,
            })
        res.update({
            'state': 'submit',
        })
        return res
     
    def write(self, vals):
        records = vals['records'] if 'records' in vals and vals['records'] else self.records
        unit_amount = vals['unit_amount'] if 'unit_amount' in vals and vals['unit_amount'] else self.unit_amount
        task_id = vals['task_id'] if 'task_id' in vals and vals['task_id'] else self.task_id.id
        if task_id:
            productivity = self.env['project.task'].browse(task_id).productivity
            if productivity and unit_amount:
                grade = round(((records / unit_amount) / productivity) * 100 ,2)
                label = self._get_grade_label(grade)
                vals.update({
                    'productivity_grade': grade,
                    'grade_label': label,
                })
        res = super(Timesheet, self).write(vals)
        return res
            
            