# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from Products.PlonePAS.sheet import MutablePropertySheet
from Products.membrane.interfaces.user import IMembraneUserProperties
from dexterity.membrane.behavior.membraneuser import MembraneUserProperties
from five import grok
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from fbk.policy.behaviors import IFBKMembraneUser
from fbk.policy.behaviors import FBKMembraneUser


class UserProperties(grok.Adapter, MembraneUserProperties, FBKMembraneUser):
    grok.context(IFBKMembraneUser)
    grok.implements(IMembraneUserProperties)

    property_map = dict(
        email='email',
        home_page='website',
        location='city',
    )

    def getPropertiesForUser(self, user, request=None):
        properties = dict(fullname=self.fullname)
        for prop_name, field_name in self.property_map.items():
            properties[prop_name] = getattr(
                self,
                field_name,
                getattr(self.context, field_name, None)) or u""

        return MutablePropertySheet(self.context.getId(), **properties)

    def setPropertiesForUser(self, user, propertysheet):
        storage = self.context

        changed = False
        properties = dict(propertysheet.propertyItems())
        for prop_name, field_name in self.property_map.items():
            value = properties.get(prop_name, '').strip()
            if value != getattr(storage, field_name, ''):
                setattr(storage, field_name, value)
                changed = True

        if changed:
            storage.reindexObject()
            notify(ObjectModifiedEvent(storage))
