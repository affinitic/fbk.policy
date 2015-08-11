# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from fbk.policy.browser.base import DefaultFieldsView
from fbk.policy.content.formationcenterfolder import IFormationCenterFolder


class FormationView(DefaultFieldsView):
    excluded_fields = (
        'title',
        'fbk_formation',
        'description',
    )

    def on_formation_center(self):
        published = self.request.get('PUBLISHED', None)
        context = getattr(published, '__parent__', None)
        if IFormationCenterFolder.providedBy(context):
            return True
        return False

    def update(self):
        self.parent = self.context.aq_parent
