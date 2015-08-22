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


class KinesiologistView(DefaultView):
    pass


class KinesiologistTraverserEditView(TraverserEditView):
    pass


class KinesiologistFieldsView(DefaultFieldsView):
    excluded_fields = (
        'lastname',
        'firstname',
        'gender',
        'photo',
        'member_type',
        'description_fr',
        'description_en',
        'description_nl',
    )

    def update(self):
        widgets = self.fieldsets['contact_informations'].widgets
        if self.can_view_email is False:
            del widgets['IMembraneContactInfos.email']
        del widgets['IMembraneContactInfos.hide_email']

    @property
    def can_view_email(self):
        result = getattr(self.context, 'hide_email', False)
        result ^= True  # Toggle the result
        return result

    @property
    def photo(self):
        return self.context.photo


class KinesiologistImages(BaseMembraneFolder):
    foldername = 'members'
    contenttype = 'kinesiologist'
    viewname = 'images'


class KinesiologistFolderView(BaseMembraneFolder):
    foldername = 'members'
    contenttype = 'kinesiologist'
    viewname = 'traverser-view'


class KinesiologistFolderEditView(BaseMembraneFolder):
    foldername = 'members'
    contenttype = 'kinesiologist'
    viewname = 'traverser-edit'
