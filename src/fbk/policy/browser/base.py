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


class ContainerView(DefaultView):
    portal_type = None
    search_depth = 1

    def update(self):
        super(ContainerView, self).update()
        catalog = api.portal.get_tool('portal_catalog')
        self.childs = catalog.searchResults(
            portal_type=self.portal_type,
            sort_on='sortable_title',
            path=self.search_path,
        )

    @property
    def search_path(self):
        current_path = '/'.join(self.context.getPhysicalPath())
        return {'query': current_path, 'depth': self.search_depth}
