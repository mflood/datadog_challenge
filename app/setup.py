#!/usr/bin/env python

from distutils.core import setup

setup(name='datadog',
      version='1.0',
      description='Datadog coding Challenge',
      author='Matthew Flood',
      author_email='matthew.data.flood@gmail.com',
      url='https://www.github.com/mflood/',
      packages=['datadog'],
      install_requires=[
          'requests',
      ],
     )
