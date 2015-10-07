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
from zope import schema

from fbk.policy import _
from fbk.policy.form.description import Description


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
    languages = schema.List(
        title=_(u'Language(s)'),
        required=True,
        value_type=schema.Choice(vocabulary='fbk.policy.languages'),
    )

    form.write_permission(member_type='cmf.ManagePortal')
    member_type = schema.Choice(
        title=_(u'Member type'),
        required=True,
        vocabulary='fbk.policy.kinesiologist.categories',
    )

    form.order_after(photo='member_type')

    description_fr = Description(
        title=_(u'Description (FR)'),
        required=False,
    )

    description_en = Description(
        title=_(u'Description (EN)'),
        required=False,
    )

    description_nl = Description(
        title=_(u'Description (NL)'),
        required=False,
    )


class Kinesiologist(Person):
    grok.implements(IKinesiologist)

    def get_title(self):
        displayed_attrs = ('lastname', 'firstname')
        displayed = [getattr(self, attr, None) for attr in displayed_attrs]
        return u' '.join([x for x in displayed if x])


class KinesiologistSchemaPolicy(grok.GlobalUtility, DexteritySchemaPolicy):
    grok.name('kinesiologist_schema_policy')

    def bases(self, schema_name, tree):
        return (IKinesiologist, )
