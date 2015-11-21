# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from fbk.policy.browser.base import DefaultFieldsView
from fbk.policy.content.kinesiologistfolder import IKinesiologistFolder


class MemberFormationView(DefaultFieldsView):
    exclude_fields = (
        'title',
        'description',
    )

    def on_member(self):
        published = self.request.get('PUBLISHED', None)
        context = getattr(published, '__parent__', None)
        if IKinesiologistFolder.providedBy(context):
            return True
        return False

    def update(self):
        self.parent = self.context.aq_parent
