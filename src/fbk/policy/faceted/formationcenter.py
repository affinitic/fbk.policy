# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from fbk.policy.faceted.base import BaseMembraneFacetedView


class FormationCenterFacetedView(BaseMembraneFacetedView):
    contenttype = 'FormationCenterFolder'

    def update(self):
        self.obj = self.get_membrane_folder()
