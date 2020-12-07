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


import os
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from .parse_config import parse_config


sql_db = SQLAlchemy()
bcrypt = Bcrypt()
l_manager = LoginManager()
l_manager.login_view = 'users.login'
l_manager.login_message_category = 'info'
mail = Mail()
data_dir = Path(
    os.path.abspath(os.path.dirname(__file__))
).joinpath('data')
config, display = parse_config(data_dir)


def create_app(config=config):
    '''
    create current_app (for multiple instances)
    '''
    current_app = Flask(__name__)
    current_app.config.from_object(config)

    from .main.routes import main
    from .users.routes import users
    from .posts.routes import posts
    from .errors.handlers import errors

    current_app.register_blueprint(main)
    current_app.register_blueprint(users)
    current_app.register_blueprint(posts)
    current_app.register_blueprint(errors)

    sql_db.init_app(current_app)
    bcrypt.init_app(current_app)
    l_manager.init_app(current_app)
    mail.init_app(current_app)
    if not Path(current_app.config['SQLALCHEMY_DATABASE_URI']
                .split("///")[1]).exists():
        sql_db.create_all(app=current_app)
    return current_app


if __name__ in ("__main__", "home_server.__main__", "home_server"):
    application = create_app()
    __all__ = [
        'current_app',
        'bcrypt'
        'l_manager',
        'sql_db',
    ]

