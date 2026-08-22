import logging

from odoo import _, http
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.http import request
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class DayflowAuthSignup(AuthSignupHome):

    @http.route(csrf=False)
    def web_login(self, *args, **kwargs):
        if request.httprequest.method == 'POST':
            login = (request.params.get('login') or '').strip()
            user = request.env['res.users'].sudo().search([('login', '=', login)], limit=1)
            employee_group = request.env.ref('dayflow_hrms.group_dayflow_employee', raise_if_not_found=False)
            if user and employee_group and employee_group in user.all_group_ids and not user.x_email_verified:
                qcontext = dict(request.params)
                qcontext.update(self.get_auth_signup_config())
                qcontext['error'] = _('Please verify your email before signing in.')
                return request.render('web.login', qcontext)
        return super().web_login(*args, **kwargs)

    def get_auth_signup_qcontext(self):
        qcontext = super().get_auth_signup_qcontext()
        qcontext['x_employee_code'] = request.params.get('x_employee_code', '')
        qcontext['dayflow_role'] = request.params.get('dayflow_role', 'employee')
        qcontext['dayflow_roles'] = [('employee', _('Employee')), ('hr', _('HR / Admin'))]
        return qcontext

    def do_signup(self, qcontext, do_login=True):
        employee_code = (qcontext.get('x_employee_code') or '').strip()
        role = qcontext.get('dayflow_role') or 'employee'
        if not employee_code:
            raise UserError(_('Employee ID is required.'))
        if role not in ('employee', 'hr'):
            raise UserError(_('Invalid Dayflow role.'))

        super().do_signup(qcontext, do_login=False)
        login = (qcontext.get('login') or '').strip()
        user = request.env['res.users'].sudo().search([('login', '=', login)], limit=1)
        if not user:
            return

        group_xmlid = 'dayflow_hrms.group_dayflow_hr' if role == 'hr' else 'dayflow_hrms.group_dayflow_employee'
        group = request.env.ref(group_xmlid)
        token = user._dayflow_new_verification_token()
        user.write({
            'x_employee_code': employee_code,
            'x_email_verified': False,
            'x_verification_token': token,
            'group_ids': [(4, group.id)],
        })
        _logger.info('Dayflow verification link: %s/dayflow/verify?token=%s',
                     request.httprequest.host_url.rstrip('/'), token)
        user._dayflow_send_verification_email()

    @http.route('/dayflow/verify', type='http', auth='public', website=True, sitemap=False)
    def dayflow_verify_email(self, token=None, **kwargs):
        user = request.env['res.users'].sudo().search([
            ('x_verification_token', '=', token),
            ('x_email_verified', '=', False),
        ], limit=1) if token else request.env['res.users']
        if not user:
            return request.render('dayflow_hrms.verification_result', {
                'success': False,
                'message': _('This verification link is invalid or has already been used.'),
            })
        user.write({'x_email_verified': True, 'x_verification_token': False})
        return request.render('dayflow_hrms.verification_result', {
            'success': True,
            'message': _('Your email has been verified. You can now sign in.'),
        })
