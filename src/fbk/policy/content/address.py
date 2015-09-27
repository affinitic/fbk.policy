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
from plone.dexterity.content import Item
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.supermodel import model
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary

from fbk.policy import _
from fbk.policy.form.zip import Zip


class IAddress(model.Schema):
    directives.languageindependent(
        'street',
        'zip_code',
        'city',
        'province',
        'country',
    )

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    street = schema.TextLine(
        title=_(u'Street'),
        required=True,
    )

    additional_address_details = schema.TextLine(
        title=_(u'Additional address details'),
        required=False,
    )

    zip_code = Zip(
        title=_(u'Zip code'),
        required=True,
    )

    city = schema.TextLine(
        title=_(u'City'),
        required=True,
    )

    province = schema.TextLine(
        title=_(u'Province'),
        required=True,
    )

    country = schema.Choice(
        title=_(u'Country'),
        required=True,
        vocabulary=SimpleVocabulary.fromValues([
            _(u'Belgium'),
            _(u'France'),
            _(u'Luxembourg'),
            _(u'Germany'),
            _(u'Nederland'),
        ]),
        default=_(u'Belgium'),
    )


class Address(Item):
    grok.implements(IAddress)


class AddressSchemaPolicy(grok.GlobalUtility, DexteritySchemaPolicy):
    grok.name('address_schema_policy')

    def bases(self, schema_name, tree):
        return (IAddress, )
