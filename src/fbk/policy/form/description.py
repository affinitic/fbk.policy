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
from z3c.form import util
from z3c.form.interfaces import IDataConverter
from z3c.form.interfaces import IWidget
from zope.schema import Text

import lxml.html

from fbk.policy.form.interfaces import IDescription


class Description(Text):
    grok.implements(IDescription)


class DescriptionConverter(converter.BaseDataConverter, grok.MultiAdapter):
    grok.adapts(IDescription, IWidget)
    grok.provides(IDataConverter)

    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return u''
        value = util.toUnicode(value)
        return value.replace('<br/>', '\r\n')

    def toFieldValue(self, value):
        if self._strip_value and isinstance(value, basestring):
            value = value.strip()
            value = unicode(lxml.html.fromstring(value).text_content())
        if value == u'':
            return self.field.missing_value
        value = self.field.fromUnicode(value)
        return '<br/>'.join(value.splitlines())
