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
from pathlib import Path
from PIL import Image
import secrets
from flask import url_for, current_app
from flask_mail import Message
from psprint import PRINT as print
from ..models import User
from .. import sql_db


def set_profile_picture(user_img, img_fname):
    '''
    Set user_img
    '''
    if img_fname == 'default.jpg':
        _, fext = os.path.splitext(user_img.filename)
        random_name = secrets.token_hex(8) + fext
        while Path(random_name).exists():
            random_name = secrets.token_hex(8) + fext
    else:
        random_name = img_fname
    output_size = (125, 125)
    small_img = Image.open(user_img)
    small_img.thumbnail(output_size)
    small_img.save(os.path.join(current_app.root_path, 'static',
                                'profile_images', random_name))
    return random_name


def send_reset_email(user: User):
    '''
    send email to user
    '''
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@anubandha.home',
                  recipients=[user.email])
    msg.body = f'''
To reset your password, visit within next 30 minutes:

the link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, ignore this email.
'''
    try:
        # mail.send(msg)
        raise(ModuleNotFoundError)
    except (ModuleNotFoundError):
        print("Mail couldn't be sent, \
supplying the necessary information on terminal", pref='err')
        print(msg, pref='bug')


def confirm_delete(user: User):
    '''
    delete user
    '''
    sql_db.session.delete(user)
    sql_db.session.commit()
    return

