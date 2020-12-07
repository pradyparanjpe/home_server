#!/usr/bin/env python3
# -*- coding: utf-8; mode:python; -*-
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



from flask import Blueprint, render_template
from .. import display


errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template("/errors/404.html", hostname=display["HOSTNAME"]), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template("/errors/403.html", hostname=display["HOSTNAME"]), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template("/errors/500.html", hostname=display["HOSTNAME"]), 500

