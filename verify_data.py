#!/usr/bin/env python3
import odoo
import odoo.tools
odoo.tools.config['db_name'] = 'Dayflow'
odoo.tools.config['db_host'] = 'odoo-db'
odoo.tools.config['db_port'] = 5432
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'
from odoo import api, SUPERUSER_ID
from odoo.modules.registry import Registry

registry = Registry('Dayflow')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    for login in ['emp1@dayflow.demo', 'emp2@dayflow.demo', 'emp3@dayflow.demo', 'emp4@dayflow.demo', 'hr@dayflow.demo']:
        user = env['res.users'].search([('login', '=', login)], limit=1)
        emp = user.employee_id if user else None
        if emp:
            payslip = env['dayflow.payroll'].search([('employee_id', '=', emp.id)], limit=1)
            leaves = env['hr.leave'].search_count([('employee_id', '=', emp.id), ('state', '=', 'confirm')])
            print(f"{emp.name}: status={emp.x_attendance_status}, pending_leave={leaves}, payroll={payslip.net_salary if payslip else 0}")
        else:
            print(f"{login}: NO EMPLOYEE")
