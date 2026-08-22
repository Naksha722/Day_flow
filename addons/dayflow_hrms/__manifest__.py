{
    'name': 'Dayflow HRMS',
    'version': '19.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Dayflow — Every workday, perfectly aligned.',
    'depends': ['base', 'mail', 'auth_signup', 'hr', 'hr_attendance', 'hr_holidays'],
    'data': [
        # --- shared ---
        'security/security_groups.xml',
        'views/dayflow_menu.xml',
        # --- avaneesh ---
        'security/ir.model.access.csv',
        'views/attendance_views.xml',
        'views/leave_views.xml',
        # --- lavanya ---
        'security/security_rules.xml',
        'views/auth_templates.xml',
        # --- samarth ---

        'views/payroll_views.xml',
        # --- naksha ---
        'views/dashboard_menu.xml',
        'views/dashboard_templates.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
