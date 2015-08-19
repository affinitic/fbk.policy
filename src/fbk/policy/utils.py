# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from plone import api
from plone.memoize import forever


@forever.memoize
def is_membrane_user(user):
    tool = api.portal.get_tool('membrane_tool')
    if tool.getUserObject(user_id=user.id):
        return True
    return False
