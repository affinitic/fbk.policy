# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from plone import api
from plone.dexterity.browser.view import DefaultView
from zope.component import getMultiAdapter


class BaseMembraneFacetedView(DefaultView):
    contenttype = None

    def get_membrane_folder(self):
        brains = api.content.find(
            context=self.lrf,
            portal_type=self.contenttype,
            id=self.context.id,
        )
        return brains[0].getObject()

    @property
    def lrf(self):
        root = api.portal.get()
        return root.get(self.language)

    @property
    def language(self):
        """
        @return: Two-letter string, the active language code
        """
        context = self.context.aq_inner
        portal_state = getMultiAdapter((context, self.request),
                                       name=u'plone_portal_state')
        current_language = portal_state.language()
        return current_language
