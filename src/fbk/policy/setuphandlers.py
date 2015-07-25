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
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility


def is_not_current_profile(context):
    return context.readDataFile('fbkpolicy_marker.txt') is None


def post_install(context):
    """Post install script"""
    if is_not_current_profile(context):
        return
    portal = api.portal.get()

    setup_languages(portal)
    delete_base_content(portal)
    create_base_content(portal)
    cleanup_contenttypes()


def setup_languages(portal):
    lang_tool = api.portal.get_tool(name='portal_languages')
    lang_tool.addSupportedLanguage('en')
    lang_tool.addSupportedLanguage('nl')

    workflow_tool = api.portal.get_tool(name='portal_workflow')
    workflow_tool.setDefaultChain('simple_publication_workflow')

    setup_tool = SetupMultilingualSite()
    setup_tool.setupSite(portal)


def delete_base_content(portal):
    """Remove the default content"""
    ids = ('Members', 'news', 'events', 'front-page')
    elements = [portal.get(id) for id in ids if id in portal]
    api.content.delete(objects=elements)


def create_base_content(portal):
    """Create the base content"""
    normalizer = getUtility(IIDNormalizer)
    fr_folder = portal['fr']
    elements = [u'Kinésiologie', u'La Fédération', u'Congrès',
                u'Kinésiologues FBK', u'Formations', u'Informations']
    for element in elements:
        element_id = normalizer.normalize(element)
        if element_id not in fr_folder:
            api.content.create(
                type='Folder',
                title=element,
                container=fr_folder,
            )


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
