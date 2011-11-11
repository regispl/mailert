#!/usr/bin/env python

from setuptools import setup

setup(name='mailert',
      version='0.1',
      description='Python Alert Mails',
      author='Michal Michalski',
      author_email='michal@michalski.im',
      url='',
      packages=['mailert'],
      keywords='mail notifier alert message',
      license='GPL',
      install_requires=[
        'setuptools',
        'smtplib',
        'email'
      ],
     )