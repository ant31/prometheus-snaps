#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'futures',
    'requests',
    'flask',
    'Flask>=0.10.1',
    'flask-cors',
    'PyYaml',

]

celery_requirements = [
    'celery[redis]',
    'celery',
]

test_requirements = [
    "pytest",
    "coverage",
    "pytest-sugar",
    "pytest-cov",
    "pytest-ordering",
    "requests-mock"
]

setup(
    name='promsnaps',
    version='0.0.1',
    description="promsnaps",
    long_description=readme,
    author="Antoine Legrand",
    author_email='2t.antoine@gmail.com',
    url='https://github.com/ant31/promsnaps',
    packages=[
        'promsnaps',
        'promsnaps.api',
        'promsnaps.api.handlers',
        'promsnaps.jobs',
    ],
    package_dir={'promsnaps':
                 'promsnaps'},
    include_package_data=True,
    install_requires=requirements + celery_requirements,
    license="Apache License version 2",
    zip_safe=False,
    keywords=['promsnaps'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
