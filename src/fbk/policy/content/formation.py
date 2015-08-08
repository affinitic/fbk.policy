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
from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy
from zope import schema
from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary

from fbk.policy import _


class IFormation(Interface):

    title = schema.TextLine(
        title=_(u'Name'),
        required=True,
    )

    description = RichText(
        title=_(u'Description'),
        required=True,
    )

    language = schema.Choice(
        title=_(u'Language'),
        required=True,
        vocabulary=SimpleVocabulary.fromValues([u'FR', u'NL', u'DE', u'EN']),
        default=u'FR',
    )

    category = schema.Choice(
        title=_(u'Category'),
        required=True,
        vocabulary=SimpleVocabulary.fromValues([
            _(u'Category 1'),
            _(u'Category 2'),
        ]),
    )


class Formation(Container):
    grok.implements(IFormation)


class FormationSchemaPolicy(grok.GlobalUtility, DexteritySchemaPolicy):
    grok.name('formation_schema_policy')

    def bases(self, schema_name, tree):
        return (IFormation, )