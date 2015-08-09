# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from plone.dexterity.browser.view import DefaultView


class FormationEventView(DefaultView):

    def update(self):
        self.parent = self.context.aq_parent
