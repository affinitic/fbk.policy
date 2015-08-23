# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from datetime import datetime
from plone import api
from plone.app.layout.viewlets import common
from fbk.policy.content.formation import IFormation
from fbk.policy.content.formationcenter import IFormationCenter
from fbk.policy.content.formationcenterfolder import IFormationCenterFolder
from fbk.policy.content.formationfbk import IFormationFBK
from fbk.policy.content.kinesiologist import IKinesiologist
from fbk.policy.content.kinesiologistfolder import IKinesiologistFolder


class BaseViewlet(common.ViewletBase):
    authorized_interfaces = []

    def can_view(self):
        for interface in self.authorized_interfaces:
            if interface.providedBy(self.context):
                return True
        return False

    def query(self, portal_type, context=None, depth=1, **kwargs):
        if context is None:
            context = self.context
        brains = api.content.find(
            portal_type=portal_type,
            context=context,
            depth=depth,
            **kwargs
        )
        return [b.getObject() for b in brains]

    def has_items(self):
        return len(self.items) > 0


class AddressViewlet(BaseViewlet):
    authorized_interfaces = (
        IFormationCenterFolder,
        IKinesiologistFolder,
    )

    def update(self):
        if self.can_view() is True:
            self.items = self.query('Address')


class FormationViewlet(BaseViewlet):
    authorized_interfaces = (
        IFormationCenterFolder,
    )

    def update(self):
        if self.can_view() is True:
            self.items = self.query('Formation', review_state='active')


class FormationFBKFormationViewlet(BaseViewlet):
    authorized_interfaces = (
        IFormationFBK,
    )

    def update(self):
        if self.can_view() is True:
            root = api.portal.get_navigation_root(self.context)
            self.items = self.query(
                'Formation',
                context=root,
                review_state='active',
                fbk_formation=self.context.id,
                depth=None,
            )


class FormationFBKViewlet(BaseViewlet):
    authorized_interfaces = (
        IFormation,
    )

    def can_view(self):
        result = super(FormationFBKViewlet, self).can_view()
        if result is True:
            if self.context.fbk_formation:
                return True
            return False
        else:
            return False

    def update(self):
        if self.can_view() is True:
            self.formationfbk = None
            root = api.portal.get_navigation_root(self.context)
            brains = api.content.find(
                portal_type='FormationFBK',
                context=root,
                id=self.context.fbk_formation,
                review_state='published',
            )
            if brains:
                self.formationfbk = brains[0].getObject()


class FormationEventViewlet(BaseViewlet):
    authorized_interfaces = (
        IFormation,
        IFormationCenterFolder,
    )

    def update(self):
        start = datetime.now()
        end = datetime.now().replace(year=start.year + 1)
        self.items = self.query(
            'FormationEvent',
            depth=2,
            start={'query': (start, end), 'range': 'min:max'},
            sort_on='start',
        )
        self.items = [i for i in self.items
                      if api.content.get_state(i.aq_parent) == 'active']


class PersonalBarViewlet(common.PersonalBarViewlet):

    def update(self):
        super(PersonalBarViewlet, self).update()
        current_user = api.user.get_current()
        tool = api.portal.get_tool('membrane_tool')
        self.membrane_object = tool.getUserObject(user_id=current_user.id)
        if self.membrane_object is not None:
            navigation_root = api.portal.get_navigation_root(self.context)
            brains = api.content.find(
                context=navigation_root,
                portal_type=self._get_portal_type(self.membrane_object),
                id=self.membrane_object.id,
            )
            self.member_folder = brains[0].getObject()

    @property
    def is_membrane_user(self):
        if hasattr(self, 'membrane_object') and self.membrane_object:
            return True
        return False

    @property
    def is_administrator(self):
        user = api.user.get_current()
        roles = user.getRoles()
        if 'Manager' in roles or 'Site Administrator' in roles:
            return True
        return False

    @property
    def membrane_user_link(self):
        if hasattr(self, 'member_folder'):
            return self.member_folder.absolute_url()
        return ''

    def _get_portal_type(self, membrane_object):
        if IFormationCenter.providedBy(membrane_object):
            return 'FormationCenterFolder'
        elif IKinesiologist.providedBy(membrane_object):
            return 'KinesiologistFolder'

    @property
    def root_url(self):
        return api.portal.get().absolute_url()
