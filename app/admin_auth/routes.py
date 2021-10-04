from flask import render_template, redirect, url_for, flash, request, session, current_app
from flask_login import current_user, login_user, logout_user, login_required
from app import db, login_manager
from app.admin_auth import bp
from app.admin_auth.email import send_password_reset_email
from app.admin_auth.models import User
from werkzeug.urls import url_parse
from datetime import datetime
from app.admin_main.shared import log


# ADMIN AUTH routes

@bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_main.index'))
    next_page = request.args.get('next')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me')

        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password','danger')
            return redirect(url_for('admin_auth.login',next=next_page))

        if remember_me == 'y':
            rem = True
        else:
            rem = False
        login_user(user, remember=rem)
        user.prev_login = user.last_login
        user.last_login = datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        flash('You are now logged in','success')

        # in case url is absolute we will ignore, we only want a relative url
        # netloc returns the www.website.com part
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('admin_main.index'))
        return redirect(url_for(next_page))

    return render_template('admin_auth/login.html', main_url=current_app.config['MAIN_URL'])


@bp.route('/logout')
@login_required
def logout():
    session.pop('edit_post',None)
    logout_user()
    flash('You are now logged out','success')
    return redirect(url_for('admin_auth.login'))


@bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('admin_auth.login'))
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        user = User(email=email, firstname=firstname, \
                    lastname=lastname, )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!','success')
        return redirect(url_for('admin_auth.login'))
    return render_template('admin_auth/register.html')


@bp.route('/forgot_password',methods=['GET','POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('admin_auth.login'))
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            if not send_password_reset_email(user):
                flash('Sorry system error','danger')
        flash('Check your email for instructions to reset your password','success')
    return render_template('admin_auth/forgot_password.html', main_url=current_app.config['MAIN_URL'])


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('admin_auth.login'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Token has expired or is no longer valid','danger')
        return redirect(url_for('admin_auth.login'))
    if request.method == 'POST':
        password = request.form.get('password')
        user.set_password(password)
        db.session.commit()
        flash('Your password has been reset','success')
        return redirect(url_for('admin_auth.login'))
    return render_template('admin_auth/reset_password.html')


# handler when you are trying to access a page but you are not logged in
@login_manager.unauthorized_handler
def unauthorized():
    #flash('You must be logged in to view this page.','danger')
    return redirect(url_for('admin_auth.login',next=request.endpoint))
