# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from five import grok
from plone.app.contenttypes.interfaces import IFolder
from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy


class IKinesiologistListing(IFolder):
    pass


class KinesiologistListing(Container):
    grok.implements(IKinesiologistListing)


class KinesiologistListingSchemaPolicy(grok.GlobalUtility,
                                       DexteritySchemaPolicy):
    grok.name('kinesiologistlisting_schema_policy')

    def bases(self, schema_name, tree):
        return (IKinesiologistListing, )
