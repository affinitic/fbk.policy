# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from Products.CMFPlone.utils import getToolByName
from plone import api
from plone.dexterity.browser.edit import DefaultEditForm
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.interfaces import IDexterityEditForm
from plone.z3cform import layout
from zope.interface import classImplements
from zope.publisher.interfaces import NotFound


class ContainerView(DefaultView):
    portal_type = None
    search_depth = 1

    def update(self):
        super(ContainerView, self).update()
        catalog = api.portal.get_tool('portal_catalog')
        self.childs = catalog.searchResults(
            portal_type=self.portal_type,
            sort_on='sortable_title',
            path=self.search_path,
        )

    @property
    def search_path(self):
        current_path = '/'.join(self.context.getPhysicalPath())
        return {'query': current_path, 'depth': self.search_depth}


class TraverserEditForm(DefaultEditForm):

    def nextURL(self):
        view_url = self.request.get('PARENTS')[0].absolute_url()
        portal_properties = getToolByName(self, 'portal_properties', None)
        if portal_properties is not None:
            site_properties = getattr(
                portal_properties,
                'site_properties',
                None
            )
            portal_type = self.portal_type
            if site_properties is not None and portal_type is not None:
                use_view_action = site_properties.getProperty(
                    'typesUseViewActionInListings',
                    ()
                )
                if portal_type in use_view_action:
                    view_url = view_url + '/view'
        return view_url


TraverserEditView = layout.wrap_form(TraverserEditForm)
classImplements(TraverserEditView, IDexterityEditForm)


class BaseMembraneFolder(DefaultView):
    """Base class for membrane folder"""
    foldername = None
    contenttype = None
    viewname = None
    notfound_error = "the {0} '{1}' does not exist"

    @property
    def base_folder(self):
        portal = api.portal.get()
        return portal.get(self.foldername)

    @property
    def id(self):
        return self.context.id

    @property
    def obj(self):
        folder = self.base_folder
        if self.id not in folder:
            raise NotFound(self.notfound_error.format(self.contenttype,
                                                      self.section))
        obj = folder.get(self.id)
        obj.translated_description = getattr(
            obj,
            'description_{0}'.format(self.context.language),
            'description_fr',
        )
        return obj

    def traverser_render(self):
        view = api.content.get_view(
            name=self.viewname,
            context=self.obj.aq_inner,
            request=self.request,
        )
        return view()


class DefaultFieldsView(DefaultView):
    excluded_fields = []

    @property
    def description(self):
        if hasattr(self.context, 'translated_description'):
            return self.context.translated_description
        return self.context.description_fr

    def updateWidgets(self):
        super(DefaultFieldsView, self).updateWidgets()
        for field in self.excluded_fields:
            if field in self.widgets:
                del self.widgets[field]
