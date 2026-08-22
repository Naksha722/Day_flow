from odoo import models, fields, api
from datetime import date, datetime, time


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    x_attendance_status = fields.Selection(
        [
            ('present', 'Present'),
            ('absent', 'Absent'),
            ('half_day', 'Half-day'),
            ('leave', 'Leave'),
        ],
        string='Today\'s Status',
        compute='_compute_x_attendance_status',
    )

    def _compute_x_attendance_status(self):
        today = date.today()
        day_start = datetime.combine(today, time.min)
        day_end = datetime.combine(today, time.max)

        for employee in self:
            # 1. Approved leave covering today wins first
            on_leave = self.env['hr.leave'].search_count([
                ('employee_id', '=', employee.id),
                ('state', '=', 'validate'),
                ('date_from', '<=', day_end),
                ('date_to', '>=', day_start),
            ])
            if on_leave:
                employee.x_attendance_status = 'leave'
                continue

            # 2. Check today's attendance record(s)
            attendances = self.env['hr.attendance'].search([
                ('employee_id', '=', employee.id),
                ('check_in', '>=', day_start),
                ('check_in', '<=', day_end),
            ])
            if not attendances:
                employee.x_attendance_status = 'absent'
                continue

            total_hours = sum(
                (att.worked_hours for att in attendances if att.worked_hours), 0.0
            )
            # Simple threshold: >=4h worked so far today = present, less = half_day.
            # Adjust the 4.0 threshold if your demo needs different behavior.
            employee.x_attendance_status = 'present' if total_hours >= 4.0 else 'half_day'
