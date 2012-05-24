# -*- coding: utf-8 -*-
"""
An alphabetical list of Swedish counties, sorted by codes.

http://en.wikipedia.org/wiki/Counties_of_Sweden

This exists in this standalone file so that it's only imported into memory
when explicitly needed.

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

COUNTY_CHOICES = (
    ('AB', _('Stockholm')),
    ('AC', _('V\xe4sterbotten')),
    ('BD', _('Norrbotten')),
    ('C', _('Uppsala')),
    ('D', _('S\xf6dermanland')),
    ('E', _('\xd6sterg\xf6tland')),
    ('F', _('J\xf6nk\xf6ping')),
    ('G', _('Kronoberg')),
    ('H', _('Kalmar')),
    ('I', _('Gotland')),
    ('K', _('Blekinge')),
    ('M', _('Sk\xe5ne')),
    ('N', _('Halland')),
    ('O', _('V\xe4stra G\xf6taland')),
    ('S', _('V\xe4rmland')),
    ('T', _('\xd6rebro')),
    ('U', _('V\xe4stmanland')),
    ('W', _('Dalarna')),
    ('X', _('G\xe4vleborg')),
    ('Y', _('V\xe4sternorrland')),
    ('Z', _('J\xe4mtland')),
)
