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
    url='https://github.com/croesnick/ansible-discover',
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
        'click',
        'ruamel.yaml',
    ],
    python_requires='>=3.6',
    packages=find_packages(exclude=['test']),
    entry_points={
        'console_scripts': [
            'ansible-discover=ansiblediscover.cli:cli',
        ]
    },
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-mock',
        'coverage',
    ],
    test_suite="test",
)
