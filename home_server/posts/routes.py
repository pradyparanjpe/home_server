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
from dateutil import parser
from flask import (Blueprint, request, flash,
                   url_for, render_template)
from flask_login import login_required, current_user
import json
from ..models import Post
from .. import sql_db, display


posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route("/todo", methods=['GET', 'POST'])
@login_required
def edit_todo():
    '''Todos'''
    if request.method == "POST":
        data = json.loads(request.data.decode('utf-8'))
        if data:
            Post.query.delete()
            for item in data:
                date =parser.parse(item['date'] or
                                   datetime.utcnow().isoformat())
                post = Post(content=item['content'],
                            status=bool(item['status']),
                            author=item['username'],
                            date=date
                            )
                sql_db.session.add(post)
            sql_db.session.commit()
            flash("Updates saved", category='success')
            return url_for('posts.edit_todo')
        flash("Error saving updates", category='danger')
    todoDB = []
    for post in Post.query.all():
        todoDB.append({'content': post.content,
                       'status': post.status,
                       'username': post.author,
                       'date': post.date})
    return render_template('todo.html', title='Lists', todoDB=todoDB,
                           hostname=display["HOSTNAME"],
                           username=current_user.username,
                           admin=int(current_user.is_admin))

