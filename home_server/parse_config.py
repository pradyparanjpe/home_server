#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-
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



from os import environ
from pathlib import Path
import yaml


class Config():
    ENV = 'production'


def yaml_conf(data_dir, yml_type):
    config_file = environ.get(f"{yml_type.upper()}_CONFIG", None)
    if config_file is None:
        config_file = data_dir.joinpath(f'{yml_type}.yaml')
    try:
        with open(config_file) as conf_handle:
            conf = yaml.safe_load(conf_handle)
    except (FileNotFoundError, AttributeError, PermissionError) as err:
        print(f"{data_dir} not found due to {err}")
        conf = {}
    return conf


def parse_config(data_dir):
    server = yaml_conf(data_dir, "server")
    display = yaml_conf(data_dir, "display")
    if 'HOSTNAME' not in display or display['HOSTNAME'] is None:
        display['HOSTNAME'] = environ['HOSTNAME']
    load_config = Config()
    db_root = Path(environ.get('db_root', f'{data_dir}/db/'))
    if not db_root.exists():
        db_root.mkdir(parents=True)
    setattr(load_config, 'SQLALCHEMY_DATABASE_URI',
            f'sqlite:///{db_root}/site.db')
    for var, setting in server.items():
        setattr(load_config, var.upper(), setting)
    return load_config, display

