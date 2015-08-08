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
from zope.schema.vocabulary import SimpleVocabulary

from fbk.policy import _


class IFormationCenter(IPerson):
    form.omitted('person_title', 'lastname', 'firstname', 'gender', 'photo')

    name = schema.TextLine(
        title=_(u'Name'),
        required=True,
    )

    category = schema.Choice(
        title=_(u'Category'),
        required=True,
        vocabulary=SimpleVocabulary.fromValues([
            _(u'Category 1'),
            _(u'Category 2'),
        ]),
    )

    form.widget(training_languages='z3c.form.browser.checkbox.CheckBoxFieldWidget')
    training_languages = schema.Choice(
        title=_(u'Training language(s)'),
        required=True,
        vocabulary=SimpleVocabulary.fromValues([u'FR', u'NL', u'DE', u'EN']),
    )

    description_fr = schema.Text(
        title=_(u'Description (FR)'),
        required=False,
    )

    description_en = schema.Text(
        title=_(u'Description (EN)'),
        required=False,
    )

    description_nl = schema.Text(
        title=_(u'Description (NL)'),
        required=False,
    )


class FormationCenter(Person):
    grok.implements(IFormationCenter)

    @property
    def title(self):
        return self.name

    @title.setter
    def title(self, value):
        return

    def Title(self):
        # must return utf8 and not unicode
        return self.title.encode('utf-8')


class FormationCenterSchemaPolicy(grok.GlobalUtility, DexteritySchemaPolicy):
    grok.name('formationcenter_schema_policy')

    def bases(self, schema_name, tree):
        return (IFormationCenter, )
