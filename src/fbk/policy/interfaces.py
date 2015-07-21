# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IFbkPolicyLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
