# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from plone import api
from plone.formwidget.namedfile.widget import NamedImageWidget
from z3c.form.widget import FieldWidget


class TraversedNamedImageWidget(NamedImageWidget):

    @property
    def download_url(self):
        if self.field is None:
            return None
        if self.ignoreContext:
            return None
        if self.filename_encoded:
            return "%s/@@edit/++widget++%s/@@download/%s" % (
                self.url, self.name, self.filename_encoded)
        else:
            return "%s/@@edit/++widget++%s/@@download" % (self.url, self.name)

    @property
    def url(self):
        portal = api.portal.get()
        members = portal.get('members')
        brains = api.content.find(
            context=members,
            portal_type='Kinesiologist',
            id=self.context.id,
        )
        return brains[0].getObject().absolute_url()


def TraversedNamedImageFieldWidget(field, request):
    return FieldWidget(field, TraversedNamedImageWidget(request))
