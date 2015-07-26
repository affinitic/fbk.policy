# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from collective.contact.core.behaviors import validateEmail
from collective.contact.core.behaviors import validatePhone
from collective.contact.membrane.behaviors.personmembraneuser import IPersonMembraneUser
from collective.contact.membrane.behaviors.personmembraneuser import PersonMembraneUser
from dexterity.membrane.behavior.membraneuser import IMembraneUserObject
from dexterity.membrane.behavior.membraneuser import IMembraneUserWorkflow
from dexterity.membrane.behavior.membraneuser import MembraneUserWorkflow
from five import grok
from plone import api
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel.directives import fieldset
from zope import schema
from zope.interface import Interface
from zope.interface import alsoProvides
from zope.interface import invariant
from zope.schema.vocabulary import SimpleVocabulary

from fbk.policy import _
from fbk.policy.exception import NotUniqueEmailAddress


class IMembraneContact(Interface):

    @invariant
    def validate_email_uniqueness(obj):
        """Ensure that the email is unique for membrane users"""
        email = obj._Data_data___.get('email')
        if email is None:
            return True
        if obj.__context__ and email == obj.__context__.email:
            return True
        if api.user.get(username=email) is not None:
            raise NotUniqueEmailAddress(email)


class IMembraneContactInfos(IMembraneContact):

    fieldset(
        'contact_informations',
        label=_(u'Contact informations'),
        fields=['email', 'phone', 'cell_phone', 'website'],
    )

    email = schema.TextLine(
        title=_(u"Email"),
        constraint=validateEmail,
        required=True,
    )

    phone = schema.TextLine(
        title=_(u"Phone"),
        required=False,
        constraint=validatePhone,
    )

    cell_phone = schema.TextLine(
        title=_(u"Cell phone"),
        required=False,
    )

    website = schema.TextLine(
        title=_(u"Website"),
        required=False,
    )

alsoProvides(IMembraneContactInfos, IFormFieldProvider)


class ICenterContactInfos(IMembraneContact):

    fieldset(
        'contact_informations',
        label=_(u'Contact informations'),
        fields=[
            'street',
            'additional_address_details',
            'zip_code',
            'city',
            'province',
            'country',
            'contact_email',
            'phone',
            'fax',
            'website',
        ],
    )

    street = schema.TextLine(
        title=_(u'Street'),
        required=True,
    )

    additional_address_details = schema.TextLine(
        title=_(u'Additional address details'),
        required=False,
    )

    zip_code = schema.Int(
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

    contact_email = schema.TextLine(
        title=_(u'Email'),
        constraint=validateEmail,
        required=False,
    )

    phone = schema.TextLine(
        title=_(u'Phone'),
        required=False,
        constraint=validatePhone,
    )

    fax = schema.TextLine(
        title=_(u'Fax'),
        required=False,
        constraint=validatePhone,
    )

    website = schema.TextLine(
        title=_(u'Website'),
        required=False,
    )

    fieldset(
        'administrator_informations',
        label=_(u'Administrator informations'),
        fields=['email', 'lastname', 'firstname'],
    )

    email = schema.TextLine(
        title=_(u'Email'),
        constraint=validateEmail,
        required=True,
    )

    lastname = schema.TextLine(
        title=_('Lastname'),
        required=True
    )

    firstname = schema.TextLine(
        title=_('Firstname'),
        required=True,
    )


alsoProvides(ICenterContactInfos, IFormFieldProvider)


class IFBKMembraneUser(IPersonMembraneUser):
    """Marker/Form interface for FBK Membrane User"""


class FBKMembraneUser(PersonMembraneUser):
    pass


class FBKMembraneUserAdapter(grok.Adapter, FBKMembraneUser):
    grok.context(IFBKMembraneUser)
    grok.implements(IMembraneUserObject)


class FBKMembraneUserWorkflow(grok.Adapter, MembraneUserWorkflow,
                              FBKMembraneUser):
    grok.context(IFBKMembraneUser)
    grok.implements(IMembraneUserWorkflow)

    allowed_states = ('active', 'deactivated')
