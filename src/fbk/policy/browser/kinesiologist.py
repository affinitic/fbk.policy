# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from plone.dexterity.browser.view import DefaultView

from fbk.policy.browser.base import BaseMembraneFolder
from fbk.policy.browser.base import TraverserEditView


class KinesiologistView(DefaultView):
    pass


class KinesiologistTraverserEditView(TraverserEditView):
    pass


class KinesiologistFieldsView(DefaultView):
    pass


class KinesiologistFolderView(BaseMembraneFolder):
    foldername = 'members'
    contenttype = 'kinesiologist'
    viewname = 'traverser-view'


class KinesiologistFolderEditView(BaseMembraneFolder):
    foldername = 'members'
    contenttype = 'kinesiologist'
    viewname = 'traverser-edit'
