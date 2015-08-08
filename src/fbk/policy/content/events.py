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
def membranetype_added(event):
    contenttype = check_contenttype(event)

    if contenttype is not None:
        create_membrane_languages_folders(
            id=event.object.id,
            title=event.object.Title(),
            type=contenttype,
        )


@grok.subscribe(IObjectRemovedEvent)
def membranetype_removed(event):
    contenttype = check_contenttype(event)

    if contenttype is not None:
        remove_membrane_languages_folders(
            id=event.object.id,
            type=contenttype,
        )


def check_contenttype(event):
    if IFormationCenter.providedBy(event.object):
        return 'FormationCenterFolder'
    if IKinesiologist.providedBy(event.object):
        return 'KinesiologistFolder'


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
