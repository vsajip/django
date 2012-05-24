# -*- coding: utf-8 -*-
"""
A list of Mexican states for use as `choices` in a formfield.

This exists in this standalone file so that it's only imported into memory
when explicitly needed.
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

# All 31 states, plus the `Distrito Federal`.
STATE_CHOICES = (
    ('AGU', _('Aguascalientes')),
    ('BCN', _('Baja California')),
    ('BCS', _('Baja California Sur')),
    ('CAM', _('Campeche')),
    ('CHH', _('Chihuahua')),
    ('CHP', _('Chiapas')),
    ('COA', _('Coahuila')),
    ('COL', _('Colima')),
    ('DIF', _('Distrito Federal')),
    ('DUR', _('Durango')),
    ('GRO', _('Guerrero')),
    ('GUA', _('Guanajuato')),
    ('HID', _('Hidalgo')),
    ('JAL', _('Jalisco')),
    ('MEX', _('Estado de M\xe9xico')),
    ('MIC', _('Michoac\xe1n')),
    ('MOR', _('Morelos')),
    ('NAY', _('Nayarit')),
    ('NLE', _('Nuevo Le\xf3n')),
    ('OAX', _('Oaxaca')),
    ('PUE', _('Puebla')),
    ('QUE', _('Quer\xe9taro')),
    ('ROO', _('Quintana Roo')),
    ('SIN', _('Sinaloa')),
    ('SLP', _('San Luis Potos\xed')),
    ('SON', _('Sonora')),
    ('TAB', _('Tabasco')),
    ('TAM', _('Tamaulipas')),
    ('TLA', _('Tlaxcala')),
    ('VER', _('Veracruz')),
    ('YUC', _('Yucat\xe1n')),
    ('ZAC', _('Zacatecas')),
)
