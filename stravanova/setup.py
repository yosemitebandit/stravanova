# -*- coding: utf-8 -*-
"""
stravanova
~~~~

This simple module condenses sets of .gpx files into a JSON form suitable for use on the Stravanova visualization site.

"""

from setuptools import setup

setup(
    name='stravanova',
    version='0.1.0',
    url='https://github.com/yosemitebandit/stravanova',
    license='BSD',
    author='Matt Ball',
    author_email='matt.ball.2@gmail.com',
    description='GPX condensing to JSON.',
    long_description=__doc__,
    py_modules=['stravanova'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
