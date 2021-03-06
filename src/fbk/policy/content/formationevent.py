# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from datetime import datetime
from five import grok
from plone import api
from plone.app.contenttypes.interfaces import IEvent
from plone.app.multilingual.dx import directives
from plone.dexterity.content import Item
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.indexer import indexer
from plone.supermodel import model
from zope import schema

from fbk.policy import _


class IFormationEvent(model.Schema, IEvent):
    directives.languageindependent(
        'start_date',
        'end_date',
        'second_start_date',
        'second_end_date',
        'price',
        'instructor',
        'training_language',
    )

    start_date = schema.Datetime(
        title=_(u'Start date'),
        required=True,
        min=datetime.now().replace(hour=0, minute=0, second=0),
        max=datetime(2030, 12, 31),
        default=datetime.now().replace(hour=0, minute=0, second=0),
    )

    end_date = schema.Datetime(
        title=_(u'End date'),
        required=True,
        min=datetime.now().replace(hour=0, minute=0, second=0),
        max=datetime(2030, 12, 31),
        default=datetime.now().replace(hour=0, minute=0, second=0),
    )

    second_start_date = schema.Datetime(
        title=_(u'Second start date'),
        required=False,
        min=datetime.now().replace(hour=0, minute=0, second=0),
        max=datetime(2030, 12, 31),
    )

    second_end_date = schema.Datetime(
        title=_(u'Second end date'),
        required=False,
        min=datetime.now().replace(hour=0, minute=0, second=0),
        max=datetime(2030, 12, 31),
    )

    price = schema.Int(
        title=_(u'Price'),
        required=True,
    )

    instructor = schema.TextLine(
        title=_(u'Instructor'),
        required=True,
    )

    training_language = schema.Choice(
        title=_(u'Language'),
        required=True,
        vocabulary='fbk.policy.languages',
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


@indexer(IFormationEvent)
def training_center(obj):
    return obj.aq_parent.aq_parent.id


@indexer(IFormationEvent)
def parent_state(obj):
    return api.content.get_state(obj.aq_parent)
