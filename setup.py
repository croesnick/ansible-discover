#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

version = '0.2.1'

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
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],
    install_requires=[
        'PyYAML~=3.12',
        'click~=6.7',
        # 0.15.59 did not work for me as it did print several 'ver (1,2)' when loading yaml
        # Until I find the underlying reason, I'll stick with a working version of ruamel.yaml
        'ruamel.yaml<=0.15.37',
    ],
    python_requires='>=3.6',
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
