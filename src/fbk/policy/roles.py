# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from borg.localrole.interfaces import ILocalRoleProvider
from dexterity.membrane.behavior.membraneuser import MembraneRoleProvider
from plone import api
from zope.component import adapter
from zope.interface import implementer

from fbk.policy.content.formationcenterfolder import IFormationCenterFolder
from fbk.policy.content.kinesiologistfolder import IKinesiologistFolder


class BaseRoleProvider(MembraneRoleProvider):
    portal_type = None

    def __init__(self, context):
        self.context = self.get_context(context)
        self.roles = self._roles()

    def get_context(self, context):
        root = api.portal.get()
        brains = api.content.find(
            portal_type=self.portal_type,
            context=root,
            depth=2,
            id=context.id,
        )
        return brains[0].getObject()


@implementer(ILocalRoleProvider)
@adapter(IFormationCenterFolder)
class FormationCenterRoleProvider(BaseRoleProvider):
    portal_type = 'FormationCenter'


@implementer(ILocalRoleProvider)
@adapter(IKinesiologistFolder)
class KinesiologistRoleProvider(BaseRoleProvider):
    portal_type = 'Kinesiologist'
