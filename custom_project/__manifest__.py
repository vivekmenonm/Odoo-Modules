# -*- coding: utf-8 -*-
{
    'name': "Project Customizations",

    'summary': """Project Customizations""",

    'description': """
        
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Project',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project', 'hr_timesheet'],

    # always loaded
    'data': [
        'security/project_security.xml',
        'security/ir.model.access.csv',
        'views/project_views.xml',
        'views/productivity_views.xml',
        'views/timesheet_views.xml',
        'report/report_productivity_report_view.xml',
        'report/report_view.xml',
        'wizard/productivity_report_wizard_view.xml',
    ],
}
