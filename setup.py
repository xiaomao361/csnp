#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File     :   setup.py
@Time     :   2023/09/14 16:39:40
@Author   :   zhouwei
@Email    :   zhouwei@linux.com
@Function :   setup file
'''

from setuptools import setup, find_packages

setup(
    name="csnp",
    version='0.0.7',
    author='zhouwei',
    author_email='xiaomao361@163.com',
    url='https://github.com/xiaomao361/csnp',
    description='crew member sentry notification plugin',
    license='MIT',
    keywords='crew sentry notification',
    include_package_data=True,
    zip_safe=False,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'sentry>10.0.1',
        'requests',
    ],
    entry_points={
        'sentry.plugins': [
            'csnp = csnp.plugin:CrewPlugin'
        ]
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ]
)
