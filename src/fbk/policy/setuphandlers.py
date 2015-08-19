# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from plone import api
from plone.app.multilingual.browser.setup import SetupMultilingualSite
from plone.app.multilingual.interfaces import ITranslationManager
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility

import collections


def is_not_current_profile(context, filepath='fbkpolicy_marker.txt'):
    return context.readDataFile(filepath) is None


def post_install(context):
    """Post install script"""
    if is_not_current_profile(context):
        return
    portal = api.portal.get()

    setup_languages(portal)
    delete_default_content(portal)
    cleanup_contenttypes()
    cleanup_actions()


def setup_languages(portal):
    lang_tool = api.portal.get_tool(name='portal_languages')
    lang_tool.addSupportedLanguage('en')
    lang_tool.addSupportedLanguage('nl')

    workflow_tool = api.portal.get_tool(name='portal_workflow')
    workflow_tool.setDefaultChain('simple_publication_workflow')

    setup_tool = SetupMultilingualSite()
    setup_tool.setupSite(portal)


def delete_default_content(portal):
    """Remove the default content"""
    ids = ('Members', 'news', 'events', 'front-page')
    elements = [portal.get(id) for id in ids if id in portal]
    api.content.delete(objects=elements)


def cleanup_contenttypes():
    """Remove collective.contact.* content types"""
    types = [
        'person',
        'directory',
        'position',
        'organization',
        'held_position',
    ]
    portal_types = api.portal.get_tool(name='portal_types')
    for t in types:
        if t in portal_types:
            del portal_types[t]


def cleanup_actions():
    """Remove unwanted actions"""
    portal_actions = api.portal.get_tool(name='portal_actions')
    object_buttons = portal_actions.object_buttons
    action_list = (
        'enable_4th_level_navigation',
        'disable_4th_level_navigation',
        'disable_direct_access',
        'enable_direct_access',
    )
    for action in action_list:
        if action in object_buttons:
            del object_buttons[action]


def setup_extra_contents(context):
    if is_not_current_profile(context, filepath='fbkpolicy_extra.txt'):
        return
    portal = api.portal.get()

    create_base_content(portal)
    setup_content_folders(portal)


def create_base_content(portal):
    """Create the base content"""
    elements = {
        u'Kinésiologues FBK': {
            'type': 'Folder',
            'childs': {
                u'Liste des kinésiologues': 'KinesiologistListing',
            },
        },
        u'Formations': {
            'type': 'Folder',
            'childs': {
                u'Liste des centres de formations': 'FormationCenterListing',
            },
        },
    }

    allow_types('KinesiologistListing', 'FormationCenterListing')
    extra_languages = ['nl', 'en']
    root_elements = {}
    for key, values in elements.items():
        container = portal['fr']
        re = create_object(key, values.get('type'), container)

        for lng in extra_languages:
            lng_container = portal[lng]
            tre = create_object(key, values.get('type'), lng_container)
            ITranslationManager(re).register_translation(lng, tre)
            root_elements[lng] = tre

        for c_title, c_type in values.get('childs', {}).items():
            e = create_object(c_title, c_type, re)

            for lng in extra_languages:
                lng_container = root_elements.get(lng)
                te = create_object(c_title, c_type, lng_container)
                ITranslationManager(e).register_translation(lng, te)

    disallow_types('KinesiologistListing', 'FormationCenterListing')


def create_object(title, type, container):
    normalizer = getUtility(IIDNormalizer)
    id = normalizer.normalize(title)
    if id not in container:
        return api.content.create(
            type=type,
            title=title,
            container=container,
        )
    return container.get(id)


def is_iterable(obj):
    return (isinstance(obj, collections.Iterable)
            and not isinstance(obj, basestring))


def setup_content_folders(portal):
    """Create base contents folders for members and formation centers"""
    allow_types('Members', 'Centers')
    if 'members' not in portal:
        api.content.create(
            type='Members',
            title='Membres',
            id='members',
            container=portal,
        )
    if 'centers' not in portal:
        api.content.create(
            type='Centers',
            title='Centres',
            id='centers',
            container=portal,
        )
    disallow_types('Members', 'Centers')


def allow_types(*types):
    portal_types = api.portal.get_tool('portal_types')
    for type in types:
        portal_types[type].global_allow = True


def disallow_types(*types):
    portal_types = api.portal.get_tool('portal_types')
    for type in types:
        portal_types[type].global_allow = False
