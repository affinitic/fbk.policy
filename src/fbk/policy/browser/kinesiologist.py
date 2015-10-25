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
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from fbk.policy.browser.base import BaseMembraneFolder
from fbk.policy.browser.base import DefaultFieldsView
from fbk.policy.browser.base import TraverserEditView


class KinesiologistView(DefaultView):
    pass


class KinesiologistTraverserEditView(TraverserEditView):
    pass


class KinesiologistFieldsView(DefaultFieldsView):
    excluded_fields = (
        'lastname',
        'firstname',
        'gender',
        'photo',
        'member_type',
        'description_fr',
        'description_en',
        'description_nl',
        'membership_fees',
        'followed_trainings',
    )

    @property
    def website_url(self):
        if self.context.website:
            if not self.context.website.startswith('http'):
                return 'http://{0}'.format(self.context.website)
            return self.context.website

    @property
    def member_type(self):
        factory = getUtility(IVocabularyFactory,
                             'fbk.policy.kinesiologist.categories')
        vocabulary = factory(self.context)
        return vocabulary.getTerm(self.context.member_type).title

    def update(self):
        widgets = self.fieldsets['contact_informations'].widgets
        if self.can_view_email is False:
            del widgets['IMembraneContactInfos.email']
        del widgets['IMembraneContactInfos.hide_email']

    @property
    def can_view_email(self):
        result = getattr(self.context, 'hide_email', False)
        result ^= True  # Toggle the result
        return result

    @property
    def photo(self):
        return self.context.photo

    @property
    def can_modify(self):
        if api.user.is_anonymous() is True:
            return False
        user = api.user.get_current()
        user_roles = api.user.get_roles(user=user, obj=self.context)
        return ('Manager' in user_roles or 'Owner' in user_roles
                or 'Editor' in user_roles)

    @property
    def is_manager(self):
        if api.user.is_anonymous() is True:
            return False
        user = api.user.get_current()
        user_roles = api.user.get_roles(user=user, obj=self.context)
        return 'Manager' in user_roles


class KinesiologistImages(BaseMembraneFolder):
    foldername = 'members'
    contenttype = 'kinesiologist'
    viewname = 'images'


class KinesiologistFolderView(BaseMembraneFolder):
    foldername = 'members'
    contenttype = 'kinesiologist'
    viewname = 'traverser-view'

    @property
    def member_type(self):
        factory = getUtility(IVocabularyFactory,
                             'fbk.policy.kinesiologist.categories')
        vocabulary = factory(self.obj)
        return vocabulary.getTerm(self.obj.member_type).title

    @property
    def cities(self):
        brains = api.content.find(
            context=self.context,
            portal_type='Address',
        )
        cities = [b.getObject().city for b in brains]
        return ' & '.join(set(cities))


class KinesiologistFolderEditView(BaseMembraneFolder):
    foldername = 'members'
    contenttype = 'kinesiologist'
    viewname = 'traverser-edit'
