# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from fbk.policy.browser.base import DefaultFieldsView


class FormationView(DefaultFieldsView):
    excluded_fields = (
        'title',
        'fbk_formation',
        'description',
    )
