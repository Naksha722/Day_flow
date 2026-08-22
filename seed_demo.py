#!/usr/bin/env python3
"""Seed demo data for Dayflow HRMS."""
import odoo
from odoo import SUPERUSER_ID

odoo.tools.config.parse_config([
    '-d', 'Dayflow',
    '--db_host=odoo-db', '--db_port=5432',
    '--db_user=odoo', '--db_password=odoo',
])

registry = odoo.registry('Dayflow')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, SUPERUSER_ID, {})

    # Get security groups
    grp_hr = env.ref('dayflow_hrms.group_dayflow_hr')
    grp_emp = env.ref('dayflow_hrms.group_dayflow_employee')

    users_data = [
        ('hr@dayflow.demo', 'Demo HR Admin', grp_hr),
        ('emp1@dayflow.demo', 'Employee One', grp_emp),
        ('emp2@dayflow.demo', 'Employee Two', grp_emp),
        ('emp3@dayflow.demo', 'Employee Three', grp_emp),
        ('emp4@dayflow.demo', 'Employee Four', grp_emp),
    ]

    employees = {}
    for login, name, group in users_data:
        user = env['res.users'].search([('login', '=', login)], limit=1)
        if not user:
            user = env['res.users'].create({
                'login': login,
                'name': name,
                'email': login,
                'password': 'emp123' if group == grp_emp else 'hr123',
                'groups_id': [(4, group.id)],
                'x_email_verified': True,
            })
            print(f'Created user: {login}')
        else:
            user.sudo().write({'x_email_verified': True})
            print(f'User exists: {login}')

        emp = env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
        if not emp:
            emp = env['hr.employee'].create({
                'name': name,
                'user_id': user.id,
            })
            print(f'Created employee: {name}')
        employees[login] = emp

    # Attendance records
    from datetime import datetime, timedelta
    now = datetime.now()

    att_data = [
        ('emp1@dayflow.demo', 9, 0, 18, 0),
        ('emp2@dayflow.demo', 13, 0, 16, 0),
        ('emp4@dayflow.demo', 9, 15, 17, 45),
    ]
    for login, ci_h, ci_m, co_h, co_m in att_data:
        emp = employees[login]
        existing = env['hr.attendance'].search([
            ('employee_id', '=', emp.id),
            ('check_in', '>=', now.replace(hour=0, minute=0, second=0)),
        ], limit=1)
        if not existing:
            env['hr.attendance'].create({
                'employee_id': emp.id,
                'check_in': now.replace(hour=ci_h, minute=ci_m, second=0),
                'check_out': now.replace(hour=co_h, minute=co_m, second=0),
            })
            print(f'Created attendance for {login}')

    # Leave requests
    leave_data = [
        ('emp1@dayflow.demo', 'Family function', 3, 4, 'confirm'),
        ('emp2@dayflow.demo', 'Fever', -2, -1, 'validate'),
        ('emp3@dayflow.demo', 'Extended trip', 10, 15, 'refuse'),
    ]
    for login, desc, from_days, to_days, state in leave_data:
        emp = employees[login]
        existing = env['hr.leave'].search([
            ('employee_id', '=', emp.id),
            ('name', '=', desc),
        ], limit=1)
        if not existing:
            today = datetime.now().date()
            env['hr.leave'].create({
                'employee_id': emp.id,
                'name': desc,
                'request_date_from': (today + timedelta(days=from_days)).strftime('%Y-%m-%d'),
                'request_date_to': (today + timedelta(days=to_days)).strftime('%Y-%m-%d'),
                'state': state,
            })
            print(f'Created leave for {login}: {desc} ({state})')

    # Payroll records
    payroll_data = [
        ('emp1@dayflow.demo', 45000, 5000, 2000, 'August 2026'),
        ('emp2@dayflow.demo', 38000, 3000, 1500, 'August 2026'),
        ('emp3@dayflow.demo', 52000, 6000, 2500, 'August 2026'),
        ('emp4@dayflow.demo', 40000, 4000, 1800, 'August 2026'),
    ]
    for login, basic, allow, ded, month in payroll_data:
        emp = employees[login]
        existing = env['dayflow.payroll'].search([
            ('employee_id', '=', emp.id),
        ], limit=1)
        if not existing:
            env['dayflow.payroll'].create({
                'employee_id': emp.id,
                'basic_salary': basic,
                'allowances': allow,
                'deductions': ded,
                'month': month,
            })
            print(f'Created payroll for {login}')

    cr.commit()
    print('\nAll demo data seeded successfully!')
