#!/usr/bin/env python
# -*- coding:utf-8; mode: python -*-
# Copyright 2020 Pradyumna Paranjape
# This file is part of home_server.
#
# home_server is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# home_server is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with home_server.  If not, see <https://www.gnu.org/licenses/>.
#



import os
from flask import (Blueprint, request, flash,
                   url_for, render_template, redirect, current_app)
from flask_login import (login_required, current_user,
                         login_user, logout_user)
from ..users.utils import (send_reset_email, set_profile_picture,
                           confirm_delete)
from ..users.forms import (RegistrationForm, LoginForm, UpdateAccount,
                           ResetPasswordForm, RequestResetForm,
                           DeleteAccountForm)
from ..models import User
from .. import bcrypt, sql_db, display


users = Blueprint('users', __name__, template_folder='templates')


@users.route('/register', methods=['GET', 'POST'])
def register():
    '''
    registration form
    '''
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pw,
            is_admin = False)
        sql_db.session.add(user)
        sql_db.session.commit()
        flash(f"Accout created for {form.username.data} you can now login",
              category='success')
        return redirect(url_for('users.login'))
    return render_template('register.html', hostname=display["HOSTNAME"],
                           title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    '''
    registration form
    '''
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if (
                user and
                bcrypt.check_password_hash(user.password, form.password.data)
        ):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next', url_for('main.home'))
            flash(f"Logged in with {form.username.data}",
                  category='success')
            return redirect(next_page)
        else:
            flash("Login Failed, check username and password",
                  category='danger')
    return render_template('login.html',
                           hostname=display["HOSTNAME"],
                           title='Login', form=form)


@users.route('/logout')
def logout():
    ''' logout '''
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    ''' account management '''
    image_file = url_for(
        'static',
        filename=(f"profile_images/{current_user.image_file}")
    )
    form = UpdateAccount()
    if form.validate_on_submit():
        if form.profile_image.data:
            random_name = set_profile_picture(
                form.profile_image.data,
                current_user.image_file
            )
            current_user.image_file = random_name
        current_user.username = form.username.data
        current_user.email = form.email.data
        sql_db.session.commit()
        flash("Your account has been updated",
              category='success')
        return redirect(url_for('users.account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account Management',
                           hostname=display["HOSTNAME"],
                           image_file=image_file, form=form)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    ''' request reset password '''
    if current_user.is_authenticated:
        flash("You are already logged in.", category='success')
        return redirect(url_for('users.account'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset password.",
              category="info")
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', hostname=display["HOSTNAME"],
                           title="Reset Password", form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    ''' request reset password '''
    if current_user.is_authenticated:
        flash("You are already logged in.", category='success')
        return redirect(url_for('users.account'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid/expired token", category='warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user.password = hashed_pw
        sql_db.session.commit()
        flash(f"Password reset for '{user.username}' you can now login",
              category='success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', hostname=display["HOSTNAME"],
                           title="Reset Password", form=form)


@users.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    '''
    delete account form
    '''
    if current_user.is_admin:
        flash("Admin account cannot be deleted", category='warning')
        return redirect(url_for('account')), 403
    next_page = request.args.get('next', url_for('main.home'))
    uname = current_user.username
    form = DeleteAccountForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(
                current_user.password, form.password.data
        ):
            user = User.query.filter_by(username=uname).first()
            logout_user();
            confirm_delete(user);
            flash(f"account for '{uname}' has been deleted.",
                  category='success')
            return redirect(next_page)
        else:
            flash("Failed. check password", category='danger')
    return render_template('delete_account.html',
                           hostname=display["HOSTNAME"],
                           title='Delete', form=form)


