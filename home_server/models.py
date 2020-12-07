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



from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from itsdangerous.exc import BadSignature
from . import sql_db, l_manager


class User(sql_db.Model, UserMixin):
    id = sql_db.Column(sql_db.Integer, primary_key=True)
    username = sql_db.Column(sql_db.String(20), unique=True, nullable=False)
    password = sql_db.Column(sql_db.String(60), nullable=False)
    email = sql_db.Column(sql_db.String(200), unique=True, nullable=False)
    image_file = sql_db.Column(sql_db.String(20), unique=False, nullable=False,
                           default='default.jpg')
    is_admin = sql_db.Column(sql_db.Boolean, nullable=False, default=False)
    # post = sql_db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, exipres_sec=1800):
        '''
        reset password token
        '''
        serial = Serializer(current_app.config['SECRET_KEY'], exipres_sec)
        return serial.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        serial = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token)['user_id']
        except (SignatureExpired, BadSignature):
            return None
        return User.query.get(user_id)

    def __repr__(self):
        '''
        print
        '''
        return f'''
        User('{self.username}', '{self.email}'),
        admin: {self.is_admin}
        '''


class Post(sql_db.Model):
    id = sql_db.Column(sql_db.Integer, primary_key=True)
    status = sql_db.Column(sql_db.Boolean)
    content = sql_db.Column(sql_db.Text)
    date = sql_db.Column(sql_db.DateTime(), nullable=False, default=datetime.utcnow)
    author = sql_db.Column(sql_db.String(20), unique=False, nullable=False)
    # userid = sql_db.Column(sql_db.Integer, sql_db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        '''
        print
        '''
        return f'''
        Post({self.id})
        {self.content},
        by {self.userid},
        on {self.date}
        '''


@l_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

