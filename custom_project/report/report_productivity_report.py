# -*- encoding: utf-8 -*-


from odoo import api, models, _
from odoo.exceptions import UserError


class ProductivityReport(models.AbstractModel):
    _name = 'report.custom_project.report_productivity_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print ("Data ; ", data)
        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        date_from = data['form'].get('date_from', False)
        date_to= data['form'].get('date_to', False)
        project_ids = data['form'].get('project_ids', False)
        employee_ids = data['form'].get('employee_ids', False) 
        
        cr = self.env.cr
        project_obj = self.env['project.project']
        task_obj = self.env['project.task']
        employee_obj = self.env['hr.employee']
        
        query = """
            SELECT pp.id AS project_id, pt.id AS task_id, emp.id AS employee_id, COUNT(aal.id) AS timesheet, SUM(aal.records) AS records, \
            SUM(aal.productivity_grade) AS grade_sum, SUM(aal.productivity_grade) / COUNT(aal.id) AS grade
            FROM account_analytic_line aal
            INNER JOIN project_project pp ON aal.project_id = pp.id
            INNER JOIN project_task pt ON aal.task_id = pt.id
            INNER JOIN hr_employee emp ON aal.employee_id = emp.id
            WHERE aal.date >= %s AND aal.date <= %s 
        """
        
        params = [date_from, date_to]
        
        if project_ids:
            query += """ AND aal.project_id IN %s """
            params.append(tuple(project_ids))
            
        if employee_ids:
            query += """ AND aal.employee_id IN %s """
            params.append(tuple(employee_ids))

        query += """ GROUP BY pp.id, pt.id, emp.id """
        
        print ("Qry ; - ", query)
        print ("Para ; - ", params)

        cr.execute(query, params)
        results = cr.dictfetchall()
        
        productivity_list = []
        timesheet_obj = self.env['account.analytic.line']
        
        print ('\nResult ; ', results)
        for line in results:
            project = project_obj.browse(line['project_id']).name
            task = task_obj.browse(line['task_id']).name
            employee = employee_obj.browse(line['employee_id']).name
            label = timesheet_obj._get_grade_label(line['grade'])
            
            productivity_list.append({'project': project, 'task': task, 'employee': employee, 'records': line['records'], 'grade': line['grade'], 'label': label})
        
        return {
            'data': data['form'],
            'productivity_list': productivity_list,
        }
        
        
