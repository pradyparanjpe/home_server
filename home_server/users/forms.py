#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-
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



from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, PasswordField, SubmitField,
                     BooleanField, validators)
from flask_login import current_user
from ..models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[
                               validators.DataRequired(),
                               validators.Length(min=2, max=20),
                           ])
    email = StringField("Email",
                        validators=[
                            validators.DataRequired(),
                            validators.Email(),
                        ])
    password = PasswordField("Password",
                             validators=[
                                 validators.DataRequired(),
                                 validators.Length(min=8),
                             ])
    confirm_pass = PasswordField("Confirm Password",
                                 validators=[
                                     validators.DataRequired(),
                                     validators.Length(min=8),
                                     validators.EqualTo('password')
                                 ])
    submit = SubmitField('Sign-up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise validators.ValidationError(
                f"'{username.data}' is taken, please choose a different one"
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise validators.ValidationError(
                f"'{email.data}' is taken, please choose a different one"
            )


class LoginForm(FlaskForm):
    username = StringField("Username",
                           validators=[
                               validators.DataRequired(),
                               validators.Length(min=2, max=20),
                           ])
    password = PasswordField("Password",
                             validators=[
                                 validators.DataRequired(),
                             ])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField('Sign-in')


class UpdateAccount(FlaskForm):
    username = StringField("Username",
                           validators=[
                               validators.DataRequired(),
                               validators.Length(min=2, max=20),
                           ])
    email = StringField("Email",
                        validators=[
                            validators.DataRequired(),
                            validators.Email(),
                        ])
    profile_image = FileField('Update Profile Picture',
                              validators=[FileAllowed(['jpg', 'png', 'bmp'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise validators.ValidationError(
                    f"\
                    '{username.data}' is taken, please choose a different one\
                    "
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise validators.ValidationError(
                    f"'{email.data}' is taken, please choose a different one"
                )


class RequestResetForm(FlaskForm):
    email = StringField("Email",
                        validators=[
                            validators.DataRequired(),
                            validators.Email(),
                        ])
    submit = SubmitField('Request Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise validators.ValidationError(
                f"'{email.data}' isn't registered.\
 Have you created an account?"
            )


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password",
                             validators=[
                                 validators.DataRequired(),
                                 validators.Length(min=8),
                             ])
    confirm_pass = PasswordField("Confirm Password",
                                 validators=[
                                     validators.DataRequired(),
                                     validators.Length(min=8),
                                     validators.EqualTo('password')
                                 ])
    submit = SubmitField('Reset')

class DeleteAccountForm(FlaskForm):
    password = PasswordField("Password",
                             validators=[
                                 validators.DataRequired(),
                             ])
    submit = SubmitField('Forget Me')

