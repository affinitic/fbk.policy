# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from Products.CMFPlone import PloneMessageFactory as PMF
from five import grok
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility
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
        brains = api.content.find(
            context=root,
            portal_type='FormationFBK',
            review_state='published',
        )

        terms = []
        for b in brains:
            terms.append(SimpleVocabulary.createTerm(
                b.id,
                b.id,
                b.Title,
            ))
        return SimpleVocabulary(terms)


class FBKFormationCenters(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name('fbk.policy.fbkformationcenters.vocabulary')

    def __call__(self, context):
        root = api.portal.get_navigation_root(context)
        brains = api.content.find(
            context=root,
            portal_type='FormationCenterFolder',
        )

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


class FBKTrainingCheck(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name('fbk.policy.training_checks')

    def __call__(self, context):
        values = {
            u'yes': PMF(u'Yes'),
            u'no': PMF(u'No'),
        }
        return dict_2_vocabulary(values)


class FBKTrainingCheckFaceted(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name('fbk.policy.training_checks.faceted')

    def __call__(self, context):
        values = {
            u'yes': PMF(u'Yes'),
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
        root = api.portal.get_navigation_root(context)
        brains = api.content.find(
            context=root,
            portal_type='FormationFBK',
            review_state='published',
        )

        terms = []
        normalizer = getUtility(IIDNormalizer)
        for b in brains:
            obj = b.getObject()
            if not obj.lessons:
                continue
            for lesson in obj.lessons.splitlines():
                lesson_id = normalizer.normalize(lesson)
                terms.append(SimpleVocabulary.createTerm(
                    '{0}|{1}'.format(b.id, lesson_id),
                    '{0}|{1}'.format(b.id, lesson_id),
                    lesson,
                ))
        return SimpleVocabulary(terms)


class KinesiologistCategories(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name('fbk.policy.kinesiologist.categories')

    def __call__(self, context):
        values = {
            'certified': _(u'Certified'),
            'certification_in_progress': _(u'Certification in progress'),
            'member': _(u'Adherent Member'),
            'honor_member': _(u'Honoured Member'),
        }
        return dict_2_vocabulary(values)
