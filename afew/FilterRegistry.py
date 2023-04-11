# SPDX-License-Identifier: ISC
# Copyright (c) Justus Winter <4winter@informatik.uni-hamburg.de>

from importlib.metadata import entry_points, EntryPoint

RAISEIT = object()


class FilterRegistry:
    """
    The FilterRegistry is responsible for returning
    filters by key.
    Filters get registered via entry points.
    To avoid any circular dependencies, the registry loads
    the Filters lazily
    """

    def __init__(self, filters):
        self.filter = {f.name: f for f in filters}

    def get(self, key, default=RAISEIT):
        if default == RAISEIT or key in self.filter:
            filter = self.filter[key]
        else:
            return default

        if isinstance(filter, EntryPoint):
            self.filter[key] = filter.load()
            return self.filter[key]
        else:
            return filter

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.filter[key] = value

    def __delitem__(self, key):
        del self.filter[key]

    def keys(self):
        return self.filter.keys()


all_filters = FilterRegistry(entry_points().select(group='afew.filter'))


def register_filter(klass):
    '''Decorator function for registering a class as a filter.'''

    all_filters[klass.__name__] = klass
    return klass
