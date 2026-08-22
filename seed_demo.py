#!/usr/bin/env python3
"""Seed demo data for Dayflow HRMS."""
import odoo
import odoo.tools
from odoo.api import SUPERUSER_ID
from odoo.modules.registry import Registry
from datetime import datetime, timedelta

odoo.tools.config['db_host'] = 'odoo-db'
odoo.tools.config['db_port'] = 5432
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'
odoo.tools.config['db_name'] = 'Dayflow'

registry = Registry('Dayflow')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, SUPERUSER_ID, {})

    grp_hr = env.ref('dayflow_hrms.group_dayflow_hr')
    grp_emp = env.ref('dayflow_hrms.group_dayflow_employee')
    grp_internal = env.ref('base.group_user')

    users_data = [
        ('hr@dayflow.demo', 'Demo HR Admin', grp_hr),
        ('emp1@dayflow.demo', 'Employee One', grp_emp),
        ('emp2@dayflow.demo', 'Employee Two', grp_emp),
        ('emp3@dayflow.demo', 'Employee Three', grp_emp),
        ('emp4@dayflow.demo', 'Employee Four', grp_emp),
    ]

    employees = {}
    for login, name, group in users_data:
        user = env['res.users'].sudo().search([('login', '=', login)], limit=1)
        if not user:
            user = env['res.users'].sudo().create({
                'login': login,
                'name': name,
                'email': login,
                'x_email_verified': True,
            })
            print(f'Created user: {login}')
        else:
            user.sudo().write({'x_email_verified': True})
            print(f'User exists: {login}')

        # Assign groups via SQL (Odoo 19 blocks groups_id in write)
        for g in [group, grp_internal]:
            cr.execute("""
                INSERT INTO res_groups_users_rel (gid, uid)
                SELECT %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM res_groups_users_rel WHERE gid = %s AND uid = %s
                )
            """, [g.id, user.id, g.id, user.id])

        # Ensure user has a company assigned (multi-company rules need this)
        company = user.company_id or env['res.company'].search([], limit=1)
        if company and company.id not in user.company_ids.ids:
            user.sudo().write({'company_ids': [(4, company.id)]})

        emp = env['hr.employee'].sudo().search([('user_id', '=', user.id)], limit=1)
        if not emp:
            emp = env['hr.employee'].sudo().create({
                'name': name,
                'user_id': user.id,
                'company_id': user.company_id.id,
            })
            print(f'Created employee: {name}')
        else:
            if not emp.company_id:
                emp.sudo().write({'company_id': user.company_id.id})
        employees[login] = emp

    # Attendance records
    now = datetime.now()

    att_data = [
        ('emp1@dayflow.demo', 9, 0, 18, 0),
        ('emp2@dayflow.demo', 13, 0, 16, 0),
        ('emp4@dayflow.demo', 9, 15, 17, 45),
    ]
    for login, ci_h, ci_m, co_h, co_m in att_data:
        emp = employees[login]
        existing = env['hr.attendance'].sudo().search([
            ('employee_id', '=', emp.id),
            ('check_in', '>=', now.replace(hour=0, minute=0, second=0)),
        ], limit=1)
        if not existing:
            env['hr.attendance'].sudo().create({
                'employee_id': emp.id,
                'check_in': now.replace(hour=ci_h, minute=ci_m, second=0),
                'check_out': now.replace(hour=co_h, minute=co_m, second=0),
            })
            print(f'Created attendance for {login}')

    # Leave type that doesn't require allocation
    leave_type = env['hr.leave.type'].sudo().search(
        [('requires_allocation', '=', False)], limit=1
    )

    # Leave requests — create via workflow, then force state via SQL
    today = datetime.now().date()
    leave_data = [
        ('emp1@dayflow.demo', 'Family function', 3, 4, 'confirm'),
        ('emp2@dayflow.demo', 'Fever', -2, -1, 'validate'),
        ('emp3@dayflow.demo', 'Extended trip', 10, 15, 'refuse'),
    ]
    for login, desc, from_days, to_days, target_state in leave_data:
        emp = employees[login]
        existing = env['hr.leave'].sudo().search([
            ('employee_id', '=', emp.id),
            ('name', '=', desc),
        ], limit=1)
        if not existing:
            leave = env['hr.leave'].sudo().create({
                'employee_id': emp.id,
                'holiday_status_id': leave_type.id if leave_type else False,
                'name': desc,
                'request_date_from': (today + timedelta(days=from_days)).strftime('%Y-%m-%d'),
                'request_date_to': (today + timedelta(days=to_days)).strftime('%Y-%m-%d'),
            })
            # Force state via SQL to avoid workflow validation issues
            cr.execute(
                "UPDATE hr_leave SET state = %s WHERE id = %s",
                [target_state, leave.id]
            )
            print(f'Created leave for {login}: {desc} ({target_state})')

    # Payroll records
    payroll_data = [
        ('emp1@dayflow.demo', 45000, 5000, 2000, 'August 2026'),
        ('emp2@dayflow.demo', 38000, 3000, 1500, 'August 2026'),
        ('emp3@dayflow.demo', 52000, 6000, 2500, 'August 2026'),
        ('emp4@dayflow.demo', 40000, 4000, 1800, 'August 2026'),
    ]
    for login, basic, allow, ded, month in payroll_data:
        emp = employees[login]
        existing = env['dayflow.payroll'].sudo().search([
            ('employee_id', '=', emp.id),
        ], limit=1)
        if not existing:
            env['dayflow.payroll'].sudo().create({
                'employee_id': emp.id,
                'basic_salary': basic,
                'allowances': allow,
                'deductions': ded,
                'month': month,
            })
            print(f'Created payroll for {login}')

    cr.commit()
    print('\nAll demo data seeded successfully!')
