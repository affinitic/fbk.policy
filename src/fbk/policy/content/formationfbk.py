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
from zope import schema
from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary

from fbk.policy import _


class IFormationFBK(Interface):

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    category = schema.Choice(
        title=_(u'Category'),
        required=True,
        vocabulary=SimpleVocabulary.fromValues([
            _(u'Category 1'),
            _(u'Category 2'),
        ]),
    )

    description = RichText(
        title=_(u'Description'),
        required=True,
    )


class FormationFBK(Item):
    pass


class FormationFBKSchemaPolicy(grok.GlobalUtility, DexteritySchemaPolicy):
    grok.name('formationfbk_schema_policy')

    def bases(self, schema_name, tree):
        return (IFormationFBK, )
