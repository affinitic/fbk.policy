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
from Products.DCWorkflow.interfaces import IAfterTransitionEvent

from fbk.policy.content.formationcenter import IFormationCenter
from fbk.policy.content.formationcenterfolder import IFormationCenterFolder
from fbk.policy.content.kinesiologist import IKinesiologist
from fbk.policy.content.kinesiologistfolder import IKinesiologistFolder


@grok.subscribe(IObjectAddedEvent)
def membranetype_added(event):
    contenttype = check_membrane_contenttype(event)

    if contenttype is not None:
        create_membrane_languages_folders(
            id=event.object.id,
            title=event.object.Title(),
            type=contenttype,
        )


@grok.subscribe(IObjectRemovedEvent)
def membranetype_removed(event):
    contenttype = check_membrane_contenttype(event)
    if not contenttype:
        contenttype = check_membrane_folder_contenttypes(event)

    if contenttype is not None:
        remove_membrane_languages_folders(
            id=event.object.id,
            type=contenttype,
        )


@grok.subscribe(IAfterTransitionEvent)
def membranetype_change_state(event):
    contenttype = check_membrane_contenttype(event)
    if not contenttype:
        contenttype = check_membrane_folder_contenttypes(event)

    if contenttype is not None:
        change_state(
            id=event.object.id,
            type=contenttype,
            transition=event.status.get('action')
        )


def check_membrane_contenttype(event):
    if IFormationCenter.providedBy(event.object):
        return 'FormationCenterFolder'
    if IKinesiologist.providedBy(event.object):
        return 'KinesiologistFolder'


def check_membrane_folder_contenttypes(event):
    if IFormationCenterFolder.providedBy(event.object):
        return 'FormationCenter'
    if IKinesiologistFolder.providedBy(event.object):
        return 'Kinesiologist'


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
    objects = [b.getObject() for b in brains]
    if objects:
        api.content.delete(objects=objects)


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


def change_state(id, type, transition):
    brains = api.content.find(portal_type=type, id=id)
    for brain in brains:
        obj = brain.getObject()
        if is_valid_transition(obj, transition) is True:
            api.content.transition(obj=obj, transition=transition)


def is_valid_transition(obj, transition):
    p_workflow = api.portal.get_tool('portal_workflow')
    chain = p_workflow.getChainFor(obj)[0]
    workflow = p_workflow.get(chain)
    current_state = api.content.get_state(obj)
    current_transitions = workflow.transitions.states.get(current_state)
    return transition in current_transitions.transitions
