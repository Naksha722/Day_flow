from odoo import models, fields, api


class DayflowPayroll(models.Model):
    _name = 'dayflow.payroll'
    _description = 'Dayflow Payroll'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', required=True, string='Employee')
    basic_salary = fields.Float(string='Basic Salary')
    allowances = fields.Float(string='Allowances')
    deductions = fields.Float(string='Deductions')
    net_salary = fields.Float(
        string='Net Salary',
        compute='_compute_net_salary',
        store=True,
    )
    month = fields.Char(string='Month')

    @api.depends('basic_salary', 'allowances', 'deductions')
    def _compute_net_salary(self):
        for rec in self:
            rec.net_salary = rec.basic_salary + rec.allowances - rec.deductions
