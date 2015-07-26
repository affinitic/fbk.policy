# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from zope.schema import ValidationError

from fbk.policy import _


class NotUniqueEmailAddress(ValidationError):
    """Exception for not unique email address"""
    __doc__ = _(u"Not unique email address")
