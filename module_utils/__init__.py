#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.facts import Facts

import os
import re
import unittest

__metaclass__ = type

# replace with $1 to strip surrounding quotes
QUOTE_STRIP = re.compile(r'^[\'\"]?([^\'\"]+)[\'\"]?$')
strip_quotes = lambda s: QUOTE_STRIP.search(s).group(1)

# TODO find a way to recursively map distributions and releases together; ie elementary's parent distro is ubuntu;
#      elementary loki's parent release is ubuntu xenial; ubuntu's parent distro is null, ubuntu xenial's parent is null
class Distribution(object):

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

class DistributionRelease(object):

    def __init__(self, name, version, distribution, parent=None):
        self.name = name
        self.version = version
        self.distribution = distribution
        self.parent = parent

# distributions
UBUNTU = Distribution('ubuntu')
ELEMENTARY = Distribution('elementary', UBUNTU)

REDHAT = Distribution('redhat')
CENTOS = Distribution('centos', REDHAT)

FEDORA = Distribution('fedora')

DISTRIBUTIONS = {
    UBUNTU.name:     UBUNTU,
    ELEMENTARY.name: ELEMENTARY,
    REDHAT.name:     REDHAT,
    CENTOS.name:     CENTOS,
    FEDORA.name:     FEDORA,
}

# releases
UBUNTU_TRUSTY = DistributionRelease('trusty', '14.04', UBUNTU)
ELEMENTARY_FREYA = DistributionRelease('freya', '0.3', ELEMENTARY, UBUNTU_TRUSTY)

UBUNTU_XENIAL = DistributionRelease('xenial', '16.04', UBUNTU)
ELEMENTARY_LOKI = DistributionRelease('loki', '0.4', ELEMENTARY, UBUNTU_XENIAL)

DISTRIBUTION_RELEASES = {
    UBUNTU_TRUSTY.name:    UBUNTU_TRUSTY,
    ELEMENTARY_FREYA.name: ELEMENTARY_FREYA,
    UBUNTU_XENIAL.name:    UBUNTU_XENIAL,
    ELEMENTARY_LOKI.name:  ELEMENTARY_LOKI,
}

def get_distribution(ansible_lsb_id):
    """Based on ansible_lsb.id, determine the distribution."""
    key = strip_quotes(ansible_lsb_id).lower()

    if key in DISTRIBUTIONS.keys():
        return DISTRIBUTIONS.get(key)
    else:
        return Distribution('unknown')


def get_root_distribution(ansible_lsb_id):
    """Based on ansible_lsb.id, determine the root distribution."""
    distribution = get_distribution(ansible_lsb_id)
    return distribution.parent if distribution.parent else distribution


def get_distribution_release(ansible_lsb_codename):
    """Based on ansible_lsb.codename, determine the distribution release."""
    return DISTRIBUTION_RELEASES.get(strip_quotes(ansible_lsb_codename).lower()) or \
        DistributionRelease('unknown', '0.0.0')


def get_root_distribution_release(ansible_lsb_codename):
    """Based on ansible_lsb.codename, determine the root distribution release."""
    release = get_distribution_release(ansible_lsb_codename)
    return release.parent if release.parent else release


class BaseFacts(Facts):

    def populate(self):
        return self.facts


class BaseFactsTestCase(unittest.TestCase):

    def test_get_distribution(self):
        """Tests that distributions are found properly."""
        centos = get_distribution('centos')
        redhat = get_distribution('redhat')
        ubuntu = get_distribution('ubuntu')
        elementary = get_distribution('elementary')
        fedora = get_distribution('fedora')

        self.assertEqual('centos', centos.name)
        self.assertEqual('redhat', redhat.name)
        self.assertEqual('redhat', centos.parent.name)

        self.assertEqual('fedora', get_distribution('fedora').name)

        self.assertEqual('ubuntu', ubuntu.name)
        self.assertEqual('ubuntu', elementary.parent.name)
        self.assertEqual('elementary', elementary.name)

        self.assertEqual('unknown', get_distribution('fhqwgads').name)

    def test_get_root_distribution(self):
        """Tests that distribution roots are found properly."""
        self.assertEqual('fedora', get_root_distribution('fedora').name)
        self.assertEqual('redhat', get_root_distribution('redhat').name)
        self.assertEqual('redhat', get_root_distribution('centos').name)
        self.assertEqual('ubuntu', get_root_distribution('elementary').name)
        self.assertEqual('ubuntu', get_root_distribution('ubuntu').name)

        self.assertEqual('unknown', get_root_distribution('fhqwgads').name)

    def test_get_distribution_release_trusty(self):
        """Tests that distribution releases are found properly."""
        # trusty
        trusty = get_distribution_release('trusty')
        self.assertEqual('trusty', trusty.name)
        self.assertEqual('14.04', trusty.version)
        self.assertIsNone(trusty.parent)
        self.assertEqual(UBUNTU, trusty.distribution)

    def test_get_distribution_release_freya(self):
        """Tests that distribution releases are found properly."""
        # freya
        freya = get_distribution_release('freya')
        self.assertEqual('freya', freya.name)
        self.assertEqual('0.3', freya.version)
        self.assertEqual(ELEMENTARY, freya.distribution)

    def test_get_distribution_release_xenial(self):
        """Tests that distribution releases are found properly."""
        # xenial
        xenial = get_distribution_release('xenial')
        self.assertEqual('xenial', xenial.name)
        self.assertEqual('16.04', xenial.version)
        self.assertEqual(UBUNTU, xenial.distribution)

    def test_get_distribution_release_loki(self):
        """Tests that distribution releases are found properly."""
        # loki
        loki = get_distribution_release('loki')
        self.assertEqual('loki', loki.name)
        self.assertEqual('0.4', loki.version)
        self.assertEqual(ELEMENTARY, loki.distribution)

    def test_get_root_distribution_release_trusty(self):
        """Tests that root distributions are found properly."""
        trusty = get_distribution_release('trusty')
