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
def searchable_text(obj):
    portal = api.portal.get()
    members = portal.get('members')
    brains = api.content.find(
        context=members,
        portal_type='Kinesiologist',
        id=obj.id,
    )
    member = brains[0].getObject()
    elements = [
        member.Title(),
        getattr(member, 'description_{0}'.format(obj.language)) or '',
    ]
    brains = api.content.find(
        context=obj,
        portal_type='Address',
        depth=1,
    )
    for brain in brains:
        address = brain.getObject()
        elements.extend([
            str(address.zip_code),
            address.city,
            address.province,
            address.country,
        ])
    return ' '.join(decode_utf8(elements))


@indexer(IKinesiologistFolder)
def countries(obj):
    brains = api.content.find(
        context=obj,
        portal_type='Address',
    )
    if brains:
        return [b.getObject().country for b in brains]


def decode_utf8(elements):
    for idx, element in enumerate(elements):
        try:
            elements[idx] = element.decode('utf8')
        except UnicodeEncodeError:
            pass
    return elements
