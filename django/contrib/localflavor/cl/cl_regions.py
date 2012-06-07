# -*- coding: utf-8 -*-
"""
A list of Chilean regions as `choices` in a formfield.

This exists in this standalone file so that it's only imported into memory
when explicitly needed.
"""
from __future__ import unicode_literals

REGION_CHOICES = (
    ('RM',  'Regi\xf3n Metropolitana de Santiago'),
    ('I',   'Regi\xf3n de Tarapac\xe1'),
    ('II',  'Regi\xf3n de Antofagasta'),
    ('III', 'Regi\xf3n de Atacama'),
    ('IV',  'Regi\xf3n de Coquimbo'),
    ('V',   'Regi\xf3n de Valpara\xedso'),
    ('VI',  'Regi\xf3n del Libertador Bernardo O\'Higgins'),
    ('VII', 'Regi\xf3n del Maule'),
    ('VIII','Regi\xf3n del B\xedo B\xedo'),
    ('IX',  'Regi\xf3n de la Araucan\xeda'),
    ('X',   'Regi\xf3n de los Lagos'),
    ('XI',  'Regi\xf3n de Ays\xe9n del General Carlos Ib\xe1\xf1ez del Campo'),
    ('XII', 'Regi\xf3n de Magallanes y la Ant\xe1rtica Chilena'),
    ('XIV', 'Regi\xf3n de Los R\xedos'),
    ('XV',  'Regi\xf3n de Arica-Parinacota'),
)
