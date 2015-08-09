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


class FBKFormations(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name('fbk.policy.fbkformations.vocabulary')

    def __call__(self, context):
        root = api.portal.get_navigation_root(context)
        brains = api.content.find(context=root, portal_type='FormationFBK')

        terms = []
        for b in brains:
            terms.append(SimpleVocabulary.createTerm(
                b.id,
                b.Title,
                b.id,
            ))
        return SimpleVocabulary(terms)
