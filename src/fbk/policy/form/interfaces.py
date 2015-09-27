# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from zope.interface import Interface


class IDescription(Interface):
    """Marker interface for description field"""


class IZip(Interface):
    """Marker interface for zip field"""
