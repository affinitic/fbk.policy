# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from OFS.interfaces import IOrderedContainer

from fbk.policy.browser.base import ListingBaseView


class ItemListingView(ListingBaseView):

    def update(self):
        super(ItemListingView, self).update()
        self.contents = sorted([c.getObject() for c in self.contents
                                if c.portal_type not in ('File', 'Image')],
                               sort_by_position)


def get_position_in_parent(obj):
    parent = obj.aq_inner.aq_parent
    ordered = IOrderedContainer(parent, None)
    if ordered is not None:
        return ordered.getObjectPosition(obj.getId())
    return 0


def sort_by_position(a, b):
    return get_position_in_parent(a) - get_position_in_parent(b)
