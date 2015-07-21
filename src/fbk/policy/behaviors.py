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
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel.directives import fieldset
from zope import schema
from zope.interface import Interface
from zope.interface import alsoProvides

from fbk.policy import _


class IContactInfos(Interface):

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

alsoProvides(IContactInfos, IFormFieldProvider)


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
