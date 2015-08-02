# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from plone.dexterity.browser.view import DefaultView
from zope.publisher.interfaces.browser import IPublishTraverse
from zope.interface import implementer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from fbk.policy.browser.base import BaseTraverser


class KinesiologistView(DefaultView):
    pass


class KinesiologistFieldsView(DefaultView):
    pass


@implementer(IPublishTraverse)
class KinesiologistTraverser(BaseTraverser):
    """Custom Traverser"""
    template = ViewPageTemplateFile('templates/kinesiologist-traversed.pt')
    foldername = 'members'
    contenttype = 'kinesiologist'
