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
from collective.z3cform.datagridfield import DictRow
from datetime import datetime
from five import grok
from plone.autoform import directives as form
from plone.dexterity.schema import DexteritySchemaPolicy
from zope import schema
from zope.interface import Interface
from zope.interface import invariant

import itertools

from fbk.policy import _
from fbk.policy import utils
from fbk.policy.content import exception
from fbk.policy.form.description import Description


class IMembershipFee(Interface):

    year = schema.Choice(
        title=_(u'Year'),
        required=True,
        vocabulary='fbk.policy.membership.fee.years',
        default=datetime.now().year,
    )

    payment = schema.Choice(
        title=_('Payment'),
        required=True,
        vocabulary='fbk.policy.membership.fee.payment',
    )


class IFollowedTraining(Interface):

    date = schema.Date(
        title=_(u'Date'),
        required=True,
        min=datetime(2015, 1, 1).date(),
        max=datetime.now().date(),
        default=datetime.now().date(),
    )

    training = schema.Choice(
        title=_(u'Lesson'),
        required=True,
        vocabulary='fbk.policy.formation.categories',
    )


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

    form.write_permission(member_type='cmf.ManagePortal')
    form.widget(membership_fees='collective.z3cform.datagridfield.DataGridFieldFactory')
    membership_fees = schema.List(
        title=_(u'Membership Fee'),
        value_type=DictRow(
            title=_(u'Membership Fee'),
            schema=IMembershipFee,
        ),
        required=False,
    )

    form.widget(followed_trainings='collective.z3cform.datagridfield.DataGridFieldFactory')
    followed_trainings = schema.List(
        title=_(u'Followed trainings'),
        value_type=DictRow(
            title=_(u'Followed trainings'),
            schema=IFollowedTraining,
        ),
        required=False,
    )

    @invariant
    def membership_fees_unicity(obj):
        value = utils.get_invariant_data(obj, 'membership_fees')
        if value is not None:
            if len(value) > len(set([e['year'] for e in value])):
                raise exception.MembershipFeeDuplicated

    @invariant
    def followed_trainings_unicty(obj):
        value = utils.get_invariant_data(obj, 'followed_trainings')
        if value is not None:
            value.sort()
            value2 = [x for x, _ in itertools.groupby(value)]
            if len(value) > len(value2):
                raise exception.FollowedTrainingDuplicated


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
