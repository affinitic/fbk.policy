# -*- coding: utf-8 -*-
"""
fbk.policy
----------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from ZTUtils import make_query
from ZTUtils import url_query
from datetime import datetime
from five import grok
from plone import api
from plone.z3ctable.batch import BatchProvider
from z3c.table.table import SequenceTable
from zope.component import getUtility
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.schema.interfaces import IVocabularyFactory

from fbk.policy.table.interfaces import IManagementTable


class Member(object):

    _properties = (
        'name',
        'membership_fee',
        'url',
        'hours',
    )

    def __init__(self, brain, year, voc):
        self.year = year
        self.vocabulary = voc
        self._convert(brain.getObject())

    def _convert(self, obj):
        """Get information from Kinesiologist object"""
        for prop in self._properties:
            setattr(self, prop, getattr(self, '_{0}'.format(prop))(obj))

    def _name(self, obj):
        if isinstance(obj.Title(), str):
            return obj.Title().decode('utf-8')
        return obj.Title()

    def _membership_fee(self, obj):
        values = obj.membership_fees or [{'year': self.year, 'payment': False}]
        value = [e.get('payment') for e in values if e['year'] == self.year]
        if not value:
            value = [False]
        return value[0]

    def _url(self, obj):
        return obj.absolute_url()

    @property
    def year_range(self):
        return range(self.year - 3, self.year)

    def _hours(self, obj):
        if not obj.followed_trainings:
            return 0.0
        value = 0.0
        trainings = [e.get('training') for e in obj.followed_trainings
                     if e.get('date').year in self.year_range]
        for training in trainings:
            try:
                term = self.vocabulary.getTerm(training)
                value += term.title
            except LookupError:
                value += 0.0
        return value


class PatientBatchProvider(BatchProvider, grok.MultiAdapter):
    grok.adapts(Interface, IBrowserRequest, Interface)
    grok.name('batch')

    def makeUrl(self, index):
        batch = self.batches[index]
        baseQuery = dict(self.request.form)
        query = {self.table.prefix + '-batchStart': batch.start,
                 self.table.prefix + '-batchSize': batch.size}
        baseQuery.update(query)
        querystring = make_query(baseQuery)
        base = url_query(self.request, omit=baseQuery.keys())
        return '%s&%s' % (base, querystring)


class ManagementTable(SequenceTable):
    grok.implements(IManagementTable)
    cssClasses = {'table': 'z3c-listing'}

    cssClassEven = u'odd'
    cssClassOdd = u'even'
    sortOn = None
    batchSize = 20
    startBatchingAt = 25
    render_none = False

    @property
    def values(self):
        brains = api.content.find(
            context=api.portal.get(),
            portal_type='Kinesiologist',
        )
        return self._filter_values(
            [Member(b, self.year, self.vocabulary) for b in brains],
        )

    def _filter_values(self, values):
        if self.membership_fee is not None:
            values = [v for v in values
                      if v.membership_fee == self.membership_fee]
        if self.hours > 0:
            values = [v for v in values
                      if v.hours <= self.hours]
        values.sort(key=lambda x: x.name)
        return values

    def get_vocabulary(self, name):
        factory = getUtility(IVocabularyFactory, name)
        return factory(self.context)

    def update(self):
        self.vocabulary = self.get_vocabulary(
            'fbk.policy.membership.trainings.hours',
        )
        self.payments = self.get_vocabulary(
            'fbk.policy.membership.fee.payment',
        )
        self.year = int(self.request.get('year', datetime.now().year))
        try:
            self.hours = float(self.request.get('hours', 0))
        except ValueError:
            self.hours = 0.0
        super(ManagementTable, self).update()

    @property
    def membership_fee(self):
        value = self.request.get('payment', '')
        if value:
            return bool(int(value))

    def render(self):
        """ Overrides of the render method from SequenceTable """
        if not len(self.rows) and self.render_none is False:
            return None
        return "%s%s%s" % (
            self.renderBatch(),
            super(ManagementTable, self).render(),
            self.renderBatch())
