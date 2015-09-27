# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from five import grok
from z3c.form import converter
from z3c.form.interfaces import IDataConverter
from z3c.form.interfaces import IWidget
from zope.schema import Int

from fbk.policy.form.interfaces import IZip


class Zip(Int):
    grok.implements(IZip)


class ZipConverter(converter.IntegerDataConverter, grok.MultiAdapter):
    grok.adapts(IZip, IWidget)
    grok.provides(IDataConverter)

    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return u''
        return unicode(value)
