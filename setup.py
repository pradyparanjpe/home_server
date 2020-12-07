#!/usr/bin/enpython3
# -*- coding: utf-8; mode:python; -*-
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install


class PostDevelop(develop):
    '''Extension for installation'''
    def run(self) -> None:
        pass


class PostInstall(install):
    '''Extension for installation'''
    def run(self) -> None:
        pass


setup(
    name="home_server",
    version="0.0.0.0dev1",
    description="Flask home server",
    license="GPLv3",
    author="Pradyumna Paranjape",
    author_email="pradyparanjpe@rediffmail.com",
    url="https://github.com/pradyparanjpe/",
    install_requires=[
        "flask", 'flask_sqlalchemy', 'flask_bcrypt', 'flask_mail',
        'flask_login', 'flask_wtf', 'wtforms', 'itsdangerous', 'Pillow',
        'psprint', 'email-validator', 'pyyaml', 'python-dateutil'
    ],
    scripts=['bin/serve.py'],
    packages=find_packages(),
)
