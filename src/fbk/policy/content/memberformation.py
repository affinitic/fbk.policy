# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from five import grok
from plone.autoform import directives as form
from plone.dexterity.content import Item
from plone.dexterity.schema import DexteritySchemaPolicy

from fbk.policy.content.formation import IFormation


class IMemberFormation(IFormation):
    form.omitted('category', 'fbk_formation')


class MemberFormation(Item):
    grok.implements(IMemberFormation)


class MemberFormationSchemaPolicy(grok.GlobalUtility, DexteritySchemaPolicy):
    grok.name('memberformation_schema_policy')

    def bases(self, schema_name, tree):
        return (IMemberFormation, )
