#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
from ansible.plugins.vars import BaseVarsPlugin

import os
import re
import unittest

__metaclass__ = type

# replace with $1 to strip surrounding quotes
QUOTE_STRIP = re.compile(r'^[\'\"]?([^\'\"]+)[\'\"]?$')
strip_quotes = lambda s: QUOTE_STRIP.search(s).group(1)

class VarsModule(BaseVarsPlugin):
    """Variable module for our custom facts."""

    def get_vars(self, loader, path, entities, cache=True):
        """Return variables."""
        result = {}

        print(entities[0].get_vars())

        return result
