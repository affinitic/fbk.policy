# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from five import grok
from plone.app.multilingual.dx import directives
from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.supermodel import model
from zope import schema

from fbk.policy import _
from fbk.policy.form.description import Description


class IFormation(model.Schema):
    directives.languageindependent('category')

    title = schema.TextLine(
        title=_(u'Name'),
        required=True,
    )

    fbk_formation = schema.Choice(
        title=_(u'Branch'),
        required=False,
        vocabulary='fbk.policy.fbkformations.vocabulary',
    )

    category = schema.Choice(
        title=_(u'Lesson'),
        required=True,
        vocabulary='fbk.policy.formation.categories',
    )

    description = Description(
        title=_(u'Description'),
        required=True,
    )


class Formation(Container):
    grok.implements(IFormation)


class FormationSchemaPolicy(grok.GlobalUtility, DexteritySchemaPolicy):
    grok.name('formation_schema_policy')

    def bases(self, schema_name, tree):
        return (IFormation, )
