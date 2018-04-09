#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

version = '0.1.0'

with open('README.rst', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='ansible-discover',
    version=version,
    description='Discover both dependants and dependencies of Ansible playbooks and roles, respectively',
    long_description=long_description,
    keywords=['ansible', 'testing', 'ci'],
    author='Carsten Rösnick-Neugebauer',
    author_email='croesnick@gmail.com',
    url='https://github.com/croesnickn/ansible-discover',
    download_url='https://github.com/croesnick/ansible-discover/archive/v{}.tar.gz'.format(version),
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],
    install_requires=[
        'PyYAML~=3.12',
        'click~=6.7',
        'ruamel.yaml~=0.15',
    ],
    python_requires='~=3.6',
    tests_require=[
        'pytest~=3.4',
        'pytest-cov~=2.5',
        'pytest-mock~=1.7',
        'coverage~=4.5',
    ],
    packages=find_packages(exclude=['test']),
    entry_points={
        'console_scripts': [
            'ansible-discover=ansiblediscover.cli:cli',
        ]
    },
    test_suite="test",
)
