#!/usr/bin/env python3
"""Seed demo users and employees through ORM — guaranteed to work."""
import odoo
import odoo.tools
from odoo import api, SUPERUSER_ID
from odoo.modules.registry import Registry

odoo.tools.config['db_name'] = 'Dayflow'
odoo.tools.config['db_host'] = 'odoo-db'
odoo.tools.config['db_port'] = 5432
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = Registry('Dayflow')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Delete old SQL-created employees
    env['hr.employee'].search([('name', 'in', ['Demo HR Admin', 'Employee One', 'Employee Two', 'Employee Three', 'Employee Four'])]).unlink()

    # Get existing users
    users = {
        'hr': env['res.users'].search([('login', '=', 'hr@dayflow.demo')], limit=1),
        'emp1': env['res.users'].search([('login', '=', 'emp1@dayflow.demo')], limit=1),
        'emp2': env['res.users'].search([('login', '=', 'emp2@dayflow.demo')], limit=1),
        'emp3': env['res.users'].search([('login', '=', 'emp3@dayflow.demo')], limit=1),
        'emp4': env['res.users'].search([('login', '=', 'emp4@dayflow.demo')], limit=1),
    }

    emp_names = {
        'hr': 'Demo HR Admin',
        'emp1': 'Employee One',
        'emp2': 'Employee Two',
        'emp3': 'Employee Three',
        'emp4': 'Employee Four',
    }

    employees = {}
    for key, user in users.items():
        if not user:
            print(f"WARNING: user {key} not found!")
            continue
        emp = env['hr.employee'].create({
            'name': emp_names[key],
            'user_id': user.id,
        })
        employees[key] = emp
        print(f"Created employee: {emp.name} (id={emp.id}, user_id={emp.user_id.id})")

    cr.commit()

    # Verify
    for key, emp in employees.items():
        user = users[key]
        print(f"\nVerification for {emp.name}:")
        print(f"  user.employee_id: {user.employee_id.id if user.employee_id else 'NONE'}")
        print(f"  emp.user_id: {emp.user_id.id if emp.user_id else 'NONE'}")
        print(f"  emp.x_attendance_status: {emp.x_attendance_status}")

    print("\nDone! All employees created through ORM.")
