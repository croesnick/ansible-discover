#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='ansible-discover',
    version='0.0.1',
    description='Discover both dependants and dependencies of Ansible playbooks and roles, respectively',
    long_description=long_description,
    keywords=['ansible', 'testing', 'ci'],
    author='Carsten Rösnick-Neugebauer',
    author_email='croesnick@gmail.com',
    url='https://github.com/croesnickn/ansible-discover',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],
    install_requires=[
        'PyYAML>=3.12',
        'click>=6.7',
    ],
    python_requires='~=3.6',
    tests_require=[
        'pytest>=3.2.3',
        'pytest-cov>=2.5.1',
        'pytest-mock>=1.6.3',
    ],
    packages=find_packages(exclude=['test']),
    entry_points={
        'console_scripts': [
            'ansible-discover=ansiblediscover.cli:cli',
        ]
    },
    test_suite="test",
)
