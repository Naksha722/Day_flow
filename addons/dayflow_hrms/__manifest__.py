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
        'security/access_avaneesh.csv',
        'views/attendance_views.xml',
        'views/leave_views.xml',
        # --- lavanya ---
        'security/security_rules.xml',
        'security/access_security.csv',
        'views/auth_templates.xml',
        # --- samarth ---
        'security/access_samarth.csv',
        'views/payroll_views.xml',
        # --- naksha ---
        'views/dashboard_menu.xml',
        'views/dashboard_templates.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
