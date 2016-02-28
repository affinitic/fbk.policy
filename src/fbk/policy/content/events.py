# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from five import grok
from plone import api
from plone.app.multilingual.interfaces import ITranslationManager
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectRemovedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from fbk.policy.content.address import IAddress
from fbk.policy.content.formation import IFormation
from fbk.policy.content.formationcenter import IFormationCenter
from fbk.policy.content.formationcenterfolder import IFormationCenterFolder
from fbk.policy.content.formationevent import IFormationEvent
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


@grok.subscribe(IObjectModifiedEvent)
def membranetype_modified(event):
    contenttype = check_membrane_contenttype(event)

    if contenttype is not None:
        portal = api.portal.get()
        brains = api.content.find(
            id=event.object.id,
            portal_type=contenttype,
            context=portal,
        )
        for b in brains:
            obj = b.getObject()
            obj.title = event.object.Title().decode('utf8')
            obj.reindexObject()


@grok.subscribe(IObjectModifiedEvent)
def formation_modified(event):
    if IFormation.providedBy(event.object):
        brains = api.content.find(
            portal_type='FormationEvent',
            context=event.object,
        )
        for b in brains:
            obj = b.getObject()
            obj.reindexObject()


@grok.subscribe(IAfterTransitionEvent)
def formation_change_state(event):
    if IFormation.providedBy(event.object):
        brains = api.content.find(
            portal_type='FormationEvent',
            contenxt=event.object,
        )
        for b in brains:
            obj = b.getObject()
            obj.reindexObject()


@grok.subscribe(IObjectAddedEvent)
def formation_event_added(event):
    if IFormationEvent.providedBy(event.object):
        obj = event.object
        parent = obj.aq_parent
        obj.name = u'{0} - {1}'.format(
            parent.title,
            obj.start_date.strftime('%d-%m-%Y'),
        )
        normalizer = getUtility(IIDNormalizer)
        id = normalizer.normalize(obj.name)
        if id in parent:
            exist = True
            idx = 0
            while exist is True:
                idx += 1
                new_id = '{0}-{1}'.format(id, idx)
                if new_id not in parent:
                    break
        else:
            new_id = id

        api.content.rename(obj=obj, new_id=new_id)


@grok.subscribe(IObjectAddedEvent)
def address_event_added(event):
    if IAddress.providedBy(event.object):
        event.object.aq_parent.reindexObject(
            idxs=['provinces', 'countries']
        )


@grok.subscribe(IObjectModifiedEvent)
def address_event_modified(event):
    if IAddress.providedBy(event.object):
        event.object.aq_parent.reindexObject(
            idxs=['provinces', 'countries']
        )


@grok.subscribe(IObjectRemovedEvent)
def address_event_removed(event):
    if IAddress.providedBy(event.object):
        event.object.aq_parent.reindexObject(
            idxs=['provinces', 'countries']
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
