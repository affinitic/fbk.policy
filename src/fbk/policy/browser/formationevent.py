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


class FormationEventView(DefaultFieldsView):
    excluded_fields = [
        'start_date',
        'end_date',
        'second_start_date',
        'second_end_date',
    ]

    date_format = '%d/%m/%Y %H:%M'

    @property
    def start_date(self):
        return self.context.start_date.strftime(self.date_format)

    @property
    def end_date(self):
        return self.context.end_date.strftime(self.date_format)

    @property
    def second_start_date(self):
        if self.context.second_start_date:
            return self.context.second_start_date.strftime(self.date_format)

    @property
    def second_end_date(self):
        if self.context.second_end_date:
            return self.context.second_end_date.strftime(self.date_format)

    def on_formation_center(self):
        published = self.request.get('PUBLISHED', None)
        context = getattr(published, '__parent__', None)
        if IFormationCenterFolder.providedBy(context):
            return True
        return False

    def update(self):
        self.parent = self.context.aq_parent
        self.formationcenter = self.parent.aq_parent
