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


class FormationCenterView(DefaultView):
    pass


class FormationCenterFieldsView(DefaultView):
    pass


@implementer(IPublishTraverse)
class FormationCenterTraverser(BaseTraverser):
    """Custom Traverser"""
    template = ViewPageTemplateFile('templates/formationcenter-traversed.pt')
    foldername = 'centers'
    contenttype = 'formationcenter'
