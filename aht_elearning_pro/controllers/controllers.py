# -*- coding: utf-8 -*-
import requests
import werkzeug

import odoo
from odoo import http, _
from odoo.addons.web.controllers.main import ensure_db, SIGN_UP_REQUEST_PARAMS, _get_login_redirect_url
from odoo.http import request


class AhtElearning(http.Controller):
    @http.route('/', website=True, auth='public')
    def home(self, **kw):
        if request.env.user.id != request.env.ref('base.public_user').id:
            return request.redirect('/web')
        return request.render('aht_elearning_pro.elearning_home')

    @http.route('/teachers', website=True, auth='public')
    def index(self, **kw):
        return request.render('aht_elearning_pro.elearning_teachers')

    @http.route('/registered', website=True, auth='public')
    def registered(self, **kw):
        user_id = request.env['res.users'].sudo().create(kw)
        teachers_group = request.env.ref('aht_elearning_pro.group_for_teachers')
        teachers_group.sudo().write({'users': [(4, user_id.id)]})
        return request.redirect('/web/login')

    def _get_login_redirect_url(uid, redirect=None):
        """ Decide if user requires a specific post-login redirect, e.g. for 2FA, or if they are
        fully logged and can proceed to the requested URL
        """
        if request.session.uid:  # fully logged
            return redirect or '/web'

        # partial session (MFA)
        url = request.env(user=uid)['res.users'].browse(uid)._mfa_url()
        if not redirect:
            return url

        parsed = werkzeug.urls.url_parse(url)
        qs = parsed.decode_query()
        qs['redirect'] = redirect
        return parsed.replace(query=werkzeug.urls.url_encode(qs)).to_url()

    def _login_redirect(self, uid, redirect=None):
        return _get_login_redirect_url(uid, redirect)

    @http.route('/register', website=True, auth='public')
    def register(self, **kwargs):
        request.env['res.users'].sudo().create(kwargs)


    @http.route('/login', type='http', auth="public", website=True)
    def login(self, redirect=None, **kw):
        ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return request.redirect(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = {k: v for k, v in request.params.items() if k in SIGN_UP_REQUEST_PARAMS}
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            try:
                uid = request.session.authenticate(request.session.db, request.params['login'],
                                                   request.params['password'])
                request.params['login_success'] = True
                return request.redirect(self._login_redirect(uid, redirect=redirect))
            except odoo.exceptions.AccessDenied as e:
                request.uid = old_uid
                if e.args == odoo.exceptions.AccessDenied().args:
                    values['error'] = _("Wrong login/password")
                else:
                    values['error'] = e.args[0]
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _('Only employees can access this database. Please contact the administrator.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        response = request.render('web.login', values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response