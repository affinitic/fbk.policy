# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from Products.CMFPlone import PloneMessageFactory as PMF
from datetime import datetime
from five import grok
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.memoize import ram
from time import time
from z3c.form.interfaces import NO_VALUE
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from fbk.policy import _
from fbk.policy import utils


def dict_2_vocabulary(dictionary):
    """Transform a dictionary into a vocabulary"""
    terms = [SimpleVocabulary.createTerm(k, k, v)
             for k, v in dictionary.items()]
    return SimpleVocabulary(terms)


class FBKFormations(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name('fbk.policy.fbkformations.vocabulary')

    def __call__(self, context):
        terms = []
        for b in fbk_formations_query(context):
            terms.append(SimpleVocabulary.createTerm(
                b.id,
                b.id,
                b.Title,
            ))
        return SimpleVocabulary(terms)


@ram.cache(lambda *args: time() // 10)
def fbk_formations_query(context):
    root = api.portal.get_navigation_root(context)
    return api.content.find(
        context=root,
        portal_type='FormationFBK',
        review_state='published',
    )


class FBKFormationCenters(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name('fbk.policy.fbkformationcenters.vocabulary')

    def __call__(self, context):
        terms = []
        for b in fbk_formation_centers_query(context):
            terms.append(SimpleVocabulary.createTerm(
                b.id,
                b.id,
                b.Title,
            ))
        return SimpleVocabulary(terms)


@ram.cache(lambda *args: time() // 10)
def fbk_formation_centers_query(context):
    root = api.portal.get_navigation_root(context)
    return api.content.find(
        context=root,
        portal_type='FormationCenterFolder',
    )


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


class FBKCountries(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name('fbk.policy.countries')

    def __call__(self, context):
        values = {
            'Belgium': _(u'Belgium'),
            'France': _(u'France'),
            'Luxembourg': _(u'Luxembourg'),
            'Germany': _(u'Germany'),
            'Nederland': _(u'Nederland'),
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
        terms = []
        normalizer = getUtility(IIDNormalizer)
        for obj in formation_categories_query(context):
            if not obj.lessons:
                continue
            for lesson in obj.lessons:
                lesson_id = normalizer.normalize(lesson['title'])
                terms.append(SimpleVocabulary.createTerm(
                    '{0}|{1}'.format(obj.id, lesson_id),
                    '{0}|{1}'.format(obj.id, lesson_id),
                    lesson['title'],
                ))
        return SimpleVocabulary(terms)


@ram.cache(lambda *args: time() // 10)
def formation_categories_query(context):
    if context == NO_VALUE or isinstance(context, dict):
        root = utils.get_navigation_root()
    else:
        root = api.portal.get_navigation_root(context)
    brains = api.content.find(
        context=root,
        portal_type='FormationFBK',
        review_state='published',
    )

    return [b.getObject() for b in brains]


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


class MembershipFeeYears(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name('fbk.policy.membership.fee.years')

    def __call__(self, context):
        values = {y: y for y in range(2015, datetime.now().year + 2)}
        return dict_2_vocabulary(values)


class MembershipFeePayment(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name('fbk.policy.membership.fee.payment')

    def __call__(self, context):
        values = {
            True: _(u'Paid'),
            False: _(u'Non paid'),
        }
        return dict_2_vocabulary(values)


class FormationHours(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name('fbk.policy.membership.trainings.hours')

    def __call__(self, context):
        terms = []
        normalizer = getUtility(IIDNormalizer)
        for obj in formation_hours_query(context):
            if not obj.lessons:
                continue
            for lesson in obj.lessons:
                lesson_id = normalizer.normalize(lesson['title'])
                terms.append(SimpleVocabulary.createTerm(
                    '{0}|{1}'.format(obj.id, lesson_id),
                    '{0}|{1}'.format(obj.id, lesson_id),
                    lesson['hours'],
                ))
        return SimpleVocabulary(terms)


@ram.cache(lambda *args: time() // 10)
def formation_hours_query(context):
    if context == NO_VALUE or isinstance(context, dict):
        root = utils.get_navigation_root()
    else:
        root = api.portal.get_navigation_root(context)
    brains = api.content.find(
        context=root,
        portal_type='FormationFBK',
    )
    return [b.getObject() for b in brains]
