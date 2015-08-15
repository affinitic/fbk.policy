# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from five import grok
from plone.app.textfield import RichText
from plone.dexterity.content import Item
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.app.multilingual.dx import directives
from zope import schema
from zope.interface import Interface

from fbk.policy import _


class IFormationFBK(Interface):
    directives.languageindependent('category')

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    category = schema.Choice(
        title=_(u'Category'),
        required=True,
        vocabulary='fbk.policy.formationfbk.categories',
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )

    text = RichText(
        title=_(u'Text'),
        required=True,
    )


class FormationFBK(Item):
    pass


class FormationFBKSchemaPolicy(grok.GlobalUtility, DexteritySchemaPolicy):
    grok.name('formationfbk_schema_policy')

    def bases(self, schema_name, tree):
        return (IFormationFBK, )
