# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from Products.Five import BrowserView
from plone import api


class FormationFBKMigrationView(BrowserView):

    def migrate(self):
        portal = api.portal.get()
        brains = api.content.find(
            portal_type='FormationFBK',
            context=portal,
        )
        for b in brains:
            obj = b.getObject()
            if obj.lessons and not isinstance(obj.lessons, list):
                obj.lessons = [{'title': t, 'hours': 0}
                               for t in obj.lessons.splitlines()]
        return u'migration finished'
