import odoo
from odoo import api, SUPERUSER_ID
from odoo.modules.registry import Registry

registry = Registry('Dayflow')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    user = env['res.users'].search([('login', '=', 'emp1@dayflow.demo')], limit=1)
    print("User:", user.id, user.login)
    print("employee_id:", user.employee_id.id if user.employee_id else "NONE")
    emp = env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
    print("Fallback emp:", emp.id if emp else "NONE")
    if emp:
        print("Name:", emp.name)
        print("Status:", emp.x_attendance_status)
        payslip = env['dayflow.payroll'].search([('employee_id', '=', emp.id)], limit=1)
        print("Payroll:", payslip.net_salary if payslip else "NONE")
        leaves = env['hr.leave'].search_count([('employee_id', '=', emp.id), ('state', '=', 'confirm')])
        print("Pending leaves:", leaves)
