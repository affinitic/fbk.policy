# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from plone import api
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


class PersonalBarViewlet(common.PersonalBarViewlet):

    def update(self):
        super(PersonalBarViewlet, self).update()
        current_user = api.user.get_current()
        tool = api.portal.get_tool('membrane_tool')
        self.membrane_object = tool.getUserObject(user_id=current_user.id)

    @property
    def is_membrane_user(self):
        if self.membrane_object is not None:
            return True
        return False

    @property
    def membrane_user_link(self):
        return self.membrane_object.absolute_url()
