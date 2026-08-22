# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class DayflowDashboard(http.Controller):

    # ------------------------------------------------------------------
    # Employee dashboard
    # ------------------------------------------------------------------
    @http.route('/dayflow/dashboard', type='http', auth='user', website=False)
    def dashboard(self, **kwargs):
        user = request.env.user
        employee = user.employee_id

        is_hr = user.has_group('dayflow_hrms.group_dayflow_hr')

        values = self._get_employee_dashboard_values(employee)
        values['is_hr'] = is_hr

        if is_hr:
            values.update(self._get_hr_dashboard_values())

        return request.render('dayflow_hrms.dashboard_template', values)

    # ------------------------------------------------------------------
    # HR: open a specific employee's own-style dashboard (read-only peek)
    # ------------------------------------------------------------------
    @http.route('/dayflow/dashboard/employee/<int:employee_id>', type='http', auth='user', website=False)
    def dashboard_employee_detail(self, employee_id, **kwargs):
        user = request.env.user
        if not user.has_group('dayflow_hrms.group_dayflow_hr'):
            return request.redirect('/dayflow/dashboard')

        employee = request.env['hr.employee'].browse(employee_id)
        values = self._get_employee_dashboard_values(employee)
        values['is_hr'] = True
        values['viewing_other_employee'] = True
        return request.render('dayflow_hrms.dashboard_template', values)

    # ------------------------------------------------------------------
    # Data helpers
    # ------------------------------------------------------------------
    def _get_employee_dashboard_values(self, employee):
        if not employee:
            return {
                'employee': None,
                'attendance_status': 'absent',
                'attendance_label': 'Absent',
                'pending_leave_count': 0,
                'net_salary': 0.0,
                'recent_activity': [],
            }

        # --- Attendance status (Checkpoint 1: real field, no fallback) ---
        attendance_status = employee.x_attendance_status or 'absent'

        attendance_label_map = {
            'present': 'Present',
            'absent': 'Absent',
            'half_day': 'Half Day',
            'leave': 'On Leave',
        }
        attendance_label = attendance_label_map.get(attendance_status, 'Unknown')

        # --- Pending leave count (real from day one) ---
        pending_leave_count = request.env['hr.leave'].search_count([
            ('employee_id', '=', employee.id),
            ('state', '=', 'confirm'),
        ])

        # --- Latest net salary (real once dayflow.payroll exists) ---
        net_salary = 0.0
        if 'dayflow.payroll' in request.env:
            payslip = request.env['dayflow.payroll'].search(
                [('employee_id', '=', employee.id)],
                order='id desc', limit=1
            )
            if payslip:
                net_salary = payslip.net_salary

        # --- Recent activity feed (placeholder per Section 7) ---
        recent_activity = [
            {'icon': 'check', 'text': 'Checked in'},
            {'icon': 'check', 'text': 'Leave approved'},
            {'icon': 'check', 'text': 'Payslip generated'},
        ]

        return {
            'employee': employee,
            'attendance_status': attendance_status,
            'attendance_label': attendance_label,
            'pending_leave_count': pending_leave_count,
            'net_salary': net_salary,
            'recent_activity': recent_activity,
        }

    def _get_hr_dashboard_values(self):
        employees = request.env['hr.employee'].search([], limit=200)
        employee_rows = []
        for emp in employees:
            attendance_status = getattr(emp, 'x_attendance_status', 'present') or 'present'
            pending_leave_count = request.env['hr.leave'].search_count([
                ('employee_id', '=', emp.id),
                ('state', '=', 'confirm'),
            ])
            employee_rows.append({
                'id': emp.id,
                'name': emp.name,
                'job_title': emp.job_title or '',
                'attendance_status': attendance_status,
                'pending_leave_count': pending_leave_count,
            })

        return {
            'employee_rows': employee_rows,
        }
