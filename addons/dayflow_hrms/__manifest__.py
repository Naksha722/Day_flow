{
    'name': 'Dayflow HRMS',
    'version': '19.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Dayflow — Every workday, perfectly aligned.',
    'depends': ['base', 'mail', 'hr', 'hr_attendance', 'hr_holidays'],
    'data': [
        # --- shared ---
        'security/security_groups.xml',
        'views/dayflow_menu.xml',
        # --- avaneesh ---
        # (added in a later step: security/ir.model.access_avaneesh.csv, views/attendance_views.xml, views/leave_views.xml)
        # --- lavanya ---
        # --- samarth ---
        # --- naksha ---
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
