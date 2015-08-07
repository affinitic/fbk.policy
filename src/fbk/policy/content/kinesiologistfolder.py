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
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy


class IKinesiologistFolder(IFolder):
    form.omitted('description')


class KinesiologistFolder(Container):
    grok.implements(IKinesiologistFolder)


class KinesiologistFolderSchemaPolicy(grok.GlobalUtility,
                                      DexteritySchemaPolicy):
    grok.name('kinesiologistfolder_schema_policy')

    def bases(self, schema_name, tree):
        return (IKinesiologistFolder, )
