# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from five import grok
from plone import api
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from fbk.policy import _


def dict_2_vocabulary(dictionary):
    """Transform a dictionary into a vocabulary"""
    terms = [SimpleVocabulary.createTerm(k, k, v)
             for k, v in dictionary.items()]
    return SimpleVocabulary(terms)


class FBKFormations(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name('fbk.policy.fbkformations.vocabulary')

    def __call__(self, context):
        root = api.portal.get_navigation_root(context)
        brains = api.content.find(context=root, portal_type='FormationFBK',
                                  review_state='published')

        terms = []
        for b in brains:
            terms.append(SimpleVocabulary.createTerm(
                b.id,
                b.id,
                b.Title,
            ))
        return SimpleVocabulary(terms)


class FBKLanguages(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name('fbk.policy.languages')

    def __call__(self, context):
        values = {
            'fr': u'FR',
            'nl': u'NL',
            'en': u'EN',
            'de': u'DE',
        }
        return dict_2_vocabulary(values)


class FBKFormationFBKCategories(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name('fbk.policy.formationfbk.categories')

    def __call__(self, context):
        values = {
            'Category 1': _(u'Category 1'),
            'Category 2': _(u'Category 2'),
        }
        return dict_2_vocabulary(values)


class FormationCategories(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name('fbk.policy.formation.categories')

    def __call__(self, context):
        values = {
            'Category 1': _(u'Category 1'),
            'Category 2': _(u'Category 2'),
        }
        return dict_2_vocabulary(values)


class FormationCenterCategories(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name('fbk.policy.formationcenter.categories')

    def __call__(self, context):
        values = {
            'Category 1': _(u'Category 1'),
            'Category 2': _(u'Category 2'),
        }
        return dict_2_vocabulary(values)


class KinesiologistCategories(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name('fbk.policy.kinesiologist.categories')

    def __call_(self, context):
        values = {
            'certified': _(u'Certified'),
            'certification_in_progress': _(u'Certification in progress'),
            'member': _(u'Member'),
        }
        return dict_2_vocabulary(values)
