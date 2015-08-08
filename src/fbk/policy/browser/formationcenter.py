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
from fbk.policy.browser.base import DefaultFieldsView
from fbk.policy.browser.base import TraverserEditView


class FormationCenterView(DefaultView):
    pass


class FormationCenterTraverserEditView(TraverserEditView):
    pass


class FormationCenterFieldsView(DefaultFieldsView):
    excluded_fields = (
        'name',
        'description_fr',
        'description_en',
        'description_nl',
    )


class FormationCenterFolderView(BaseMembraneFolder):
    foldername = 'centers'
    contenttype = 'formationcenter'
    viewname = 'traverser-view'


class FormationCenterFolderEditView(BaseMembraneFolder):
    foldername = 'centers'
    contenttype = 'formationcenter'
    viewname = 'traverser-edit'