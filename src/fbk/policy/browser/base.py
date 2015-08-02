# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from plone import api
from plone.dexterity.browser.view import DefaultView
from Products.Five.browser import BrowserView
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


class BaseTraverser(BrowserView):
    """Base class for formation center and kinesiologist traversers"""
    foldername = None
    contenttype = None
    notfound_error = "the {0} '{1}' does not exist"

    @property
    def base_folder(self):
        portal = api.portal.get()
        return portal.get(self.foldername)

    def __init__(self, context, request):
        super(BaseTraverser, self).__init__(context, request)
        if len(request.path) == 2:
            [self.section, profileid] = request.path
        elif len(self.request.path) == 1:
            self.section = request.path[0]

    def __call__(self):
        folder = self.base_folder
        if self.section not in folder:
            raise NotFound(self.notfound_error.format(self.contenttype,
                                                      self.section))
        obj = folder.get(self.section)
        obj.description = getattr(
            obj,
            'description_{0}'.format(self.context.language),
            'description_fr',
        )
        self.obj = obj
        self.request.set('traversed', True)
        self.request.set('traversed_title', obj.Title())
        return self.template()

    def publishTraverse(self, request, name):
        # stop traversing, we have arrived
        request['TraversalRequestNameStack'] = []
        # return self so the publisher calls this view
        return self

    def traverse_render(self):
        view = api.content.get_view(
            name='traverser-view',
            context=self.obj.aq_inner,
            request=self.request,
        )
        return view()
