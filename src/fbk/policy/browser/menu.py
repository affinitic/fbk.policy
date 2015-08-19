# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from plone import api
from plone.app.contentmenu import menu
from plone.app.multilingual.browser.menu import TranslateMenu
from eea.facetednavigation.layout.menu import FacetedDisplayMenu

from fbk.policy import utils
from fbk.policy.content.formationcenter import IFormationCenter
from fbk.policy.content.formationcenterfolder import IFormationCenterFolder
from fbk.policy.content.kinesiologist import IKinesiologist
from fbk.policy.content.kinesiologistfolder import IKinesiologistFolder


class MenuMixin(object):
    membrane_interfaces = (
        IFormationCenter,
        IFormationCenterFolder,
        IKinesiologist,
        IKinesiologistFolder,
    )

    excluded_items = ()

    def is_membrane_object(self, obj):
        for interface in self.membrane_interfaces:
            if interface.providedBy(obj):
                return True
        return False

    @property
    def is_membrane_user(self):
        user = api.user.get_current()
        return utils.is_membrane_user(user)

    def filter_items(self, items):
        return [e for e in items
                if e['extra']['id'] not in self.excluded_items]


class ActionsMenu(MenuMixin, menu.ActionsMenu):
    excluded_items = (
        'plone-contentmenu-actions-copy',
        'plone-contentmenu-actions-cut',
        'plone-contentmenu-actions-faceted.enable',
        'plone-contentmenu-actions-faceted.search.enable',
    )

    def getMenuItems(self, obj, request):
        items = super(ActionsMenu, self).getMenuItems(obj, request)
        if self.is_membrane_object(obj):
            return []
        if self.is_membrane_user:
            items = self.filter_items(items)
        return items


class TranslationMenu(MenuMixin, TranslateMenu):
    excluded_items = (
        '_universal_link',
        '_shared_folder',
        '_edit_babel_edit',
    )

    def getMenuItems(self, obj, request):
        items = super(TranslationMenu, self).getMenuItems(obj, request)
        if self.is_membrane_object(obj):
            return []
        if self.is_membrane_user:
            items = self.filter_items(items)
        return items


class DisplayMenu(MenuMixin, FacetedDisplayMenu):

    def getMenuItems(self, obj, request):
        items = super(DisplayMenu, self).getMenuItems(obj, request)
        if self.is_membrane_object(obj):
            items = []
        return items
