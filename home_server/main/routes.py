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
import yaml
from flask import (Blueprint, render_template, send_from_directory)
from psprint import PRINT as print
from .. import display


main = Blueprint('main', '__name__')


@main.route('/')
@main.route('/home')
@main.route('/index')
def home() -> str:
    '''
    hello world
    '''
    return render_template('index.html', hostname=display['HOSTNAME'],
                           display=display, title='Home')

