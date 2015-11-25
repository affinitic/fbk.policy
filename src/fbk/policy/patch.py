# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from datetime import datetime
from plone.formwidget.datetime.z3cform.widget import DateWidget


def date_widget_update(self):
    now = datetime.now()
    min_value = -10
    max_value = 10
    if self.field.min:
        min_value = self.field.min.year - now.year
    if self.field.max:
        max_value = self.field.max.year - now.year + 1
    self.years_range = (min_value, max_value)
    super(DateWidget, self).update()
