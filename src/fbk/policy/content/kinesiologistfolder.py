# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from five import grok
from plone import api
from plone.app.contenttypes.interfaces import IFolder
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.indexer import indexer


class IKinesiologistFolder(IFolder):
    form.omitted('description')


class KinesiologistFolder(Container):
    grok.implements(IKinesiologistFolder)


class KinesiologistFolderSchemaPolicy(grok.GlobalUtility,
                                      DexteritySchemaPolicy):
    grok.name('kinesiologistfolder_schema_policy')

    def bases(self, schema_name, tree):
        return (IKinesiologistFolder, )


@indexer(IKinesiologistFolder)
def provinces(obj):
    brains = api.content.find(
        context=obj,
        portal_type='Address',
    )
    if brains:
        return [b.getObject().province for b in brains]


@indexer(IKinesiologistFolder)
def languages(obj):
    portal = api.portal.get()
    members = portal.get('members')
    brains = api.content.find(
        context=members,
        portal_type='Kinesiologist',
        id=obj.id,
    )
    return brains[0].getObject().languages


@indexer(IKinesiologistFolder)
def description(obj):
    portal = api.portal.get()
    members = portal.get('members')
    brains = api.content.find(
        context=members,
        portal_type='Kinesiologist',
        id=obj.id,
    )
    lang = obj.language
    return getattr(brains[0].getObject(), 'description_{0}'.format(lang))
