# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from five import grok
from z3c.table import column
from z3c.table.interfaces import IColumn
from zope.interface import Interface
from zope.i18n import translate

from fbk.policy import _
from fbk.policy.table.interfaces import IManagementTable


class NameColumn(column.GetAttrColumn, grok.MultiAdapter):
    grok.provides(IColumn)
    grok.name('name')
    grok.adapts(Interface, Interface, IManagementTable)

    header = _(u'Lastname & firstname')
    weight = 10

    def _value(self, item):
        return item.name

    def renderCell(self, item):
        return u'<a href="{0}">{1}</a>'.format(
            item.url,
            self._value(item),
        )


class YearColumn(column.GetAttrColumn, grok.MultiAdapter):
    grok.provides(IColumn)
    grok.name('year')
    grok.adapts(Interface, Interface, IManagementTable)

    header = _(u'Year')
    weight = 15

    def renderCell(self, item):
        return self.table.year


class CotisationColumn(column.GetAttrColumn, grok.MultiAdapter):
    grok.provides(IColumn)
    grok.name('membership-fee')
    grok.adapts(Interface, Interface, IManagementTable)

    header = _(u'Membership fee')
    weight = 20

    def renderCell(self, item):
        value = self.table.payments.getTerm(item.membership_fee).title
        return translate(value, context=self.request)


class TrainingHoursColumn(column.GetAttrColumn, grok.MultiAdapter):
    grok.provides(IColumn)
    grok.name('training-hours')
    grok.adapts(Interface, Interface, IManagementTable)

    header = _(u'Training Hours (last 3 years)')
    weight = 30
    attrName = 'hours'
