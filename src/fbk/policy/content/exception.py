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


class MembershipFeeDuplicated(ValidationError):
    __doc__ = _(u'There is a duplicated membership fee for a year')


class FollowedTrainingDuplicated(ValidationError):
    __doc__ = _(u'There is a duplicated followed training')
