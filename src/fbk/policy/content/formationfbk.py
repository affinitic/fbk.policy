# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from collective.z3cform.datagridfield import DictRow
from five import grok
from plone.app.textfield import RichText
from plone.autoform import directives as form
from plone.dexterity.content import Item
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.supermodel import model
from zope import schema
from zope.interface import Interface

from fbk.policy import _


class ILesson(Interface):

    title = schema.TextLine(
        title=_(u'Name'),
        required=True,
    )

    hours = schema.Int(
        title=_(u'Hours'),
        required=True,
        default=0,
    )


class IFormationFBK(model.Schema):

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )

    text = RichText(
        title=_(u'Text'),
        required=True,
    )

    form.widget(lessons='collective.z3cform.datagridfield.DataGridFieldFactory')
    lessons = schema.List(
        title=_(u'Lessons'),
        value_type=DictRow(
            title=_(u'Lessons'),
            schema=ILesson,
        ),
        required=False,
    )


class FormationFBK(Item):
    pass


class FormationFBKSchemaPolicy(grok.GlobalUtility, DexteritySchemaPolicy):
    grok.name('formationfbk_schema_policy')

    def bases(self, schema_name, tree):
        return (IFormationFBK, )
