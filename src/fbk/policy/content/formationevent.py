# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from five import grok
from plone.app.contenttypes.interfaces import IEvent
from plone.dexterity.content import Item
from plone.dexterity.schema import DexteritySchemaPolicy
from zope import schema

from fbk.policy import _


class IFormationEvent(IEvent):

    start_date = schema.Datetime(
        title=_(u'Start date'),
        required=True,
    )

    end_date = schema.Datetime(
        title=_(u'End date'),
        required=True,
    )

    price = schema.Int(
        title=_(u'Price'),
        required=True,
    )

    instructor = schema.TextLine(
        title=_(u'Instructor'),
        required=True,
    )

    training_check = schema.Bool(
        title=_(u'Training check'),
        required=False,
    )


class FormationEvent(Item):
    grok.implements(IFormationEvent)

    @property
    def title(self):
        return getattr(self, 'name', '')

    @title.setter
    def title(self, value):
        return

    def Title(self):
        # must return utf8 and not unicode
        return self.title.encode('utf-8')


class FormationEventSchemaPolicy(grok.GlobalUtility, DexteritySchemaPolicy):
    grok.name('formationevent_schema_policy')

    def bases(self, schema_name, tree):
        return (IFormationEvent, )
