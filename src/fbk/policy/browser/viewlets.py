# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from plone.app.layout.viewlets import common


class BaseTraversedViewlet(object):

    @property
    def traversed(self):
        return self.request.get('traversed')


class PathBarViewlet(BaseTraversedViewlet, common.PathBarViewlet):

    @property
    def traversed_title(self):
        return self.request.get('traversed_title')

    def update(self):
        super(PathBarViewlet, self).update()
        if self.traversed:
            self.breadcrumbs += ({
                'absolute_url': '',
                'Title': self.traversed_title},
            )


class ContentViewsViewlet(BaseTraversedViewlet, common.ContentViewsViewlet):

    def render(self):
        if self.traversed:
            return ''
        return super(ContentViewsViewlet, self).render()


class ContentActionsViewlet(BaseTraversedViewlet, common.ContentActionsViewlet):

    def render(self):
        if self.traversed:
            return ''
        return super(ContentActionsViewlet, self).render()
