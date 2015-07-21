# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from collective.contact.core.content.person import IPerson
from collective.contact.core.content.person import Person
from five import grok
from plone.autoform import directives as form
from plone.dexterity.schema import DexteritySchemaPolicy
from zope.schema.vocabulary import SimpleVocabulary
from zope import schema

from fbk.policy import _


class IKinesiologist(IPerson):
    form.omitted('person_title')

    lastname = schema.TextLine(
        title=_("Lastname"),
        required=True
    )

    firstname = schema.TextLine(
        title=_("Firstname"),
        required=True,
    )

    gender = schema.Choice(
        title=_("Gender"),
        vocabulary="Genders",
        required=True,
    )

    form.widget(languages='z3c.form.browser.checkbox.CheckBoxFieldWidget')
    languages = schema.Choice(
        title=_(u'Language(s)'),
        required=True,
        vocabulary=SimpleVocabulary.fromValues([u'FR', u'NL', u'DE', u'EN']),
    )

    member_type = schema.Choice(
        title=_(u'Member type'),
        required=True,
        vocabulary=SimpleVocabulary.fromValues([
            _(u'Certified'),
            _(u'Certification in progress'),
            _(u'Member'),
        ]),
    )

    form.order_after(photo='member_type')


class Kinesiologist(Person):
    grok.implements(IKinesiologist)


class KinesiologistSchemaPolicy(grok.GlobalUtility, DexteritySchemaPolicy):
    grok.name('kinesiologist_schema_policy')

    def bases(self, schema_name, tree):
        return (IKinesiologist, )
