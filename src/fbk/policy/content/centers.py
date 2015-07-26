# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from collective.contact.core.content.directory import Directory
from collective.contact.core.content.directory import IDirectory
from five import grok
from plone.autoform import directives as form
from plone.dexterity.schema import DexteritySchemaPolicy


class ICenters(IDirectory):
    form.omitted('position_types', 'organization_types', 'organization_levels')


class Centers(Directory):
    grok.implements(ICenters)


class CentersSchemaPolicy(grok.GlobalUtility, DexteritySchemaPolicy):
    grok.name('centers_schema_policy')

    def bases(self, schema_name, tree):
        return (ICenters, )
