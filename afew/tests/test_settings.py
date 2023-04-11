# SPDX-License-Identifier: ISC
# Copyright (c) 2013 Patrick Gerken <do3cc@patrick-gerken.de>

from importlib.metadata import EntryPoint
import unittest


class TestFilterRegistry(unittest.TestCase):

    def test_all_filters_exist(self):
        from afew import FilterRegistry
        self.assertTrue(hasattr(FilterRegistry.all_filters, 'get'))

    def test_entry_point_registration(self):
        from afew import FilterRegistry

        class FakeEntryPoint(EntryPoint):
            def load(self):
                return self.value

        registry = FilterRegistry.FilterRegistry([FakeEntryPoint(name='test', value='class', group='')])

        self.assertEqual('class', registry['test'])

    def test_add_FilterRegistry(self):
        from afew import FilterRegistry
        try:
            FilterRegistry.all_filters['test'] = 'class'
            self.assertEqual('class', FilterRegistry.all_filters['test'])
        finally:
            del FilterRegistry.all_filters['test']
