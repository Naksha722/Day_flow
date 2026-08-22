import uuid

from odoo import _, api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    x_employee_code = fields.Char(string='Employee ID', copy=False, index=True)
    x_email_verified = fields.Boolean(string='Email Verified', default=False, copy=False)
    x_verification_token = fields.Char(string='Verification Token', copy=False, index=True)

    @api.model
    def _dayflow_new_verification_token(self):
        return uuid.uuid4().hex

    def _dayflow_send_verification_email(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for user in self:
            if not user.x_verification_token:
                user.sudo().x_verification_token = self._dayflow_new_verification_token()
            verification_url = '%s/dayflow/verify?token=%s' % (
                base_url.rstrip('/'),
                user.x_verification_token,
            )
            self.env['mail.mail'].sudo().create({
                'subject': _('Verify your Dayflow account'),
                'email_to': user.email or user.login,
                'body_html': _(
                    '<p>Welcome to Dayflow.</p>'
                    '<p><a href="%(url)s">Verify your email address</a></p>'
                    '<p>If the button does not work, open: %(url)s</p>',
                    url=verification_url,
                ),
            })
