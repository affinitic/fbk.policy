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
from plone.app.multilingual.interfaces import ITranslationManager
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectRemovedEvent

from fbk.policy.content.kinesiologist import IKinesiologist
from fbk.policy.content.formationcenter import IFormationCenter


@grok.subscribe(IObjectAddedEvent)
def formationcenter_added(event):
    if IFormationCenter.providedBy(event.object):
        create_membrane_languages_folders(
            id=event.object.id,
            title=event.object.Title(),
            type='FormationCenterFolder',
        )


@grok.subscribe(IObjectRemovedEvent)
def formationcenter_removed(event):
    if IFormationCenter.providedBy(event.object):
        remove_membrane_languages_folders(
            id=event.object.id,
            type='FormationCenterFolder',
        )


@grok.subscribe(IObjectAddedEvent)
def kinesiologist_added(event):
    if IKinesiologist.providedBy(event.object):
        create_membrane_languages_folders(
            id=event.object.id,
            title=event.object.Title(),
            type='KinesiologistFolder',
        )


@grok.subscribe(IObjectRemovedEvent)
def kinesiologist_removed(event):
    if IKinesiologist.providedBy(event.object):
        remove_membrane_languages_folders(
            id=event.object.id,
            type='KinesiologistFolder',
        )


def create_membrane_languages_folders(**kwargs):
    elements = []
    for lng in get_languages():
        container = get_container(kwargs.get('type'), lng)
        element = api.content.create(
            container=container,
            **kwargs
        )
        if len(elements) > 0:
            first_e = elements[0]
            ITranslationManager(first_e).register_translation(lng, element)
        elements.append(element)


def remove_membrane_languages_folders(id, type):
    brains = api.content.find(portal_type=type, id=id)
    api.content.delete(objects=[b.getObject() for b in brains])


def get_container(type, language):
    """Return the container for the current type and language"""
    search_type = type.replace('Folder', 'Listing')
    portal = api.portal.get()
    result = api.content.find(
        context=portal[language],
        portal_type=search_type,
        depth=2,
    )
    return result[0].getObject()


def get_languages():
    """Return the active languages"""
    portal_languages = api.portal.get_tool('portal_languages')
    return portal_languages.supported_langs
