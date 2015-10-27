# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from Products.Five import BrowserView
from datetime import datetime

from fbk.policy import _
from fbk.policy.table.management import ManagementTable


class MemberManagementView(BrowserView):

    def url(self):
        return '{0}?{1}'.format(
            self.request.get('ACTUAL_URL'),
            self.request.get('QUERY_STRING'),
        )

    def get_table_render(self):
        table = ManagementTable(self.context, self.request)
        table.update()
        render = table.render()
        if not render:
            render = _('No result for selected filters')
        return render

    def get_years(self):
        return range(2015, datetime.now().year + 2)

    @property
    def hours(self):
        return self.request.get('hours', '')

    def get_membership_fees(self):
        return (
            (_(u'All'), ''),
            (_(u'Paid'), '1'),
            (_(u'Non paid'), '0'),
        )
