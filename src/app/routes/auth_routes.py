from flask import Blueprint, render_template, redirect,url_for, flash
from flask_login import login_required, logout_user

from src.app.services.auth_service import AuthService, ServiceError
from src.app.forms.auth_form import LoginForm

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            AuthService.validation(
                username=form.username.data, 
                password=form.password.data
            )
            return redirect(url_for('admin_panel.show_registers'))

        except ServiceError as e:
            flash(str(e), 'danger')

    return render_template('auth/login.html', form=form)


@bp.route('/logout/user')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))