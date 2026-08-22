from odoo import http
from odoo.http import request


class DayflowDashboard(http.Controller):

    @http.route('/dayflow/dashboard', type='http', auth='user', website=False)
    def dashboard(self, **kwargs):
        user = request.env.user
        employee = user.employee_id

        # Determine if user is HR/Admin
        is_hr = user.has_group('dayflow_hrms.group_dayflow_hr')

        values = {
            'employee': employee,
            'user': user,
            'is_hr': is_hr,
        }

        if is_hr:
            values.update(self._get_hr_dashboard_data(employee))
        else:
            values.update(self._get_employee_dashboard_data(employee))

        return request.render('dayflow_hrms.dashboard_template', values)

    def _get_employee_dashboard_data(self, employee):
        """Gather data for the employee dashboard view."""
        if not employee:
            return {
                'attendance_status': 'absent',
                'pending_leave_count': 0,
                'approved_leave_count': 0,
                'net_salary': 0,
                'recent_activities': [],
            }

        # Attendance status
        attendance_status = employee.x_attendance_status or 'absent'

        # Pending leave count for this employee
        pending_leave_count = request.env['hr.leave'].search_count([
            ('employee_id', '=', employee.id),
            ('state', '=', 'confirm'),
        ])

        # Approved leave count for this employee
        approved_leave_count = request.env['hr.leave'].search_count([
            ('employee_id', '=', employee.id),
            ('state', '=', 'validate'),
        ])

        # Latest payroll net_salary (Samarth's model — check if it exists)
        net_salary = 0
        try:
            payroll = request.env['dayflow.payroll'].search([
                ('employee_id', '=', employee.id),
            ], order='create_date desc', limit=1)
            if payroll:
                net_salary = payroll.net_salary
        except Exception:
            pass

        # Recent activities (latest attendance + leave records)
        recent_activities = []

        # Latest attendance
        latest_att = request.env['hr.attendance'].search([
            ('employee_id', '=', employee.id),
        ], order='check_in desc', limit=1)
        if latest_att:
            if latest_att.check_out:
                recent_activities.append({
                    'icon': '✓',
                    'text': 'Checked out at %s' % latest_att.check_out.strftime('%I:%M %p'),
                    'color': 'success',
                })
            else:
                recent_activities.append({
                    'icon': '✓',
                    'text': 'Checked in at %s' % latest_att.check_in.strftime('%I:%M %p'),
                    'color': 'success',
                })

        # Latest leave
        latest_leave = request.env['hr.leave'].search([
            ('employee_id', '=', employee.id),
        ], order='create_date desc', limit=1)
        if latest_leave:
            state_map = {
                'draft': 'Leave request drafted',
                'confirm': 'Leave request pending',
                'validate': 'Leave approved',
                'refuse': 'Leave rejected',
            }
            color_map = {
                'draft': 'muted',
                'confirm': 'warning',
                'validate': 'success',
                'refuse': 'danger',
            }
            recent_activities.append({
                'icon': '✓',
                'text': state_map.get(latest_leave.state, 'Leave updated'),
                'color': color_map.get(latest_leave.state, 'muted'),
            })

        return {
            'attendance_status': attendance_status,
            'pending_leave_count': pending_leave_count,
            'approved_leave_count': approved_leave_count,
            'net_salary': net_salary,
            'recent_activities': recent_activities,
        }

    def _get_hr_dashboard_data(self, employee):
        """Gather data for the HR/Admin dashboard view."""
        # All employees
        all_employees = request.env['hr.employee'].search([])

        # Summary counts
        total_employees = len(all_employees)
        present_today = len(all_employees.filtered(
            lambda e: e.x_attendance_status == 'present'))
        absent_today = len(all_employees.filtered(
            lambda e: e.x_attendance_status == 'absent'))
        on_leave_today = len(all_employees.filtered(
            lambda e: e.x_attendance_status == 'leave'))

        # Pending leave requests (all employees)
        pending_leaves = request.env['hr.leave'].search([
            ('state', '=', 'confirm'),
        ])

        # Employee list with status for the table
        employee_list = []
        for emp in all_employees:
            emp_pending = request.env['hr.leave'].search_count([
                ('employee_id', '=', emp.id),
                ('state', '=', 'confirm'),
            ])
            employee_list.append({
                'id': emp.id,
                'name': emp.name,
                'job': emp.job_id.name if emp.job_id else '',
                'department': emp.department_id.name if emp.department_id else '',
                'attendance_status': emp.x_attendance_status or 'absent',
                'pending_leaves': emp_pending,
            })

        # Self dashboard data (for the greeting + personal cards)
        self_data = {}
        if employee:
            self_data = self._get_employee_dashboard_data(employee)

        return {
            **self_data,
            'total_employees': total_employees,
            'present_today': present_today,
            'absent_today': absent_today,
            'on_leave_today': on_leave_today,
            'pending_leaves': pending_leaves,
            'employee_list': employee_list,
        }
