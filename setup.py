# -*- coding: utf-8 -*-
"""Installer for the fbk.policy package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')


setup(
    name='fbk.policy',
    version='0.1',
    description="Policy for Kinesiology Belgium website",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3.6",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='Python Plone',
    author='Martin Peeters',
    author_email='martin.peeters@affinitic.be',
    url='http://github.com/affinitic/fbk.policy',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['fbk'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'collective.contact.core',
        'collective.contact.membrane',
        'eea.facetednavigation',
        'five.grok',
        'plone.api',
        'plone.app.dexterity',
        'plone.autoform',
        'setuptools',
        'z3c.jbot',
        'plone.app.multilingual',
        'plone.app.contenttypes',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    """,
)
