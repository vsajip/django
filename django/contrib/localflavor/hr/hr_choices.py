# -*- coding: utf-8 -*-
"""
Sources:
    Croatian Counties: http://en.wikipedia.org/wiki/ISO_3166-2:HR

    Croatia doesn't have official abbreviations for counties.
    The ones provided are in common use.
"""
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

HR_COUNTY_CHOICES = (
    ('GZG', _('Grad Zagreb')),
    ('BB\u017d', _('Bjelovarsko-bilogorska \u017eupanija')),
    ('BP\u017d', _('Brodsko-posavska \u017eupanija')),
    ('DN\u017d', _('Dubrova\u010dko-neretvanska \u017eupanija')),
    ('I\u017d', _('Istarska \u017eupanija')),
    ('K\u017d', _('Karlova\u010dka \u017eupanija')),
    ('KK\u017d', _('Koprivni\u010dko-kri\u017eeva\u010dka \u017eupanija')),
    ('KZ\u017d', _('Krapinsko-zagorska \u017eupanija')),
    ('LS\u017d', _('Li\u010dko-senjska \u017eupanija')),
    ('M\u017d', _('Me\u0111imurska \u017eupanija')),
    ('OB\u017d', _('Osje\u010dko-baranjska \u017eupanija')),
    ('PS\u017d', _('Po\u017ee\u0161ko-slavonska \u017eupanija')),
    ('PG\u017d', _('Primorsko-goranska \u017eupanija')),
    ('SM\u017d', _('Sisa\u010dko-moslava\u010dka \u017eupanija')),
    ('SD\u017d', _('Splitsko-dalmatinska \u017eupanija')),
    ('\u0160K\u017d', _('\u0160ibensko-kninska \u017eupanija')),
    ('V\u017d', _('Vara\u017edinska \u017eupanija')),
    ('VP\u017d', _('Viroviti\u010dko-podravska \u017eupanija')),
    ('VS\u017d', _('Vukovarsko-srijemska \u017eupanija')),
    ('ZD\u017d', _('Zadarska \u017eupanija')),
    ('ZG\u017d', _('Zagreba\u010dka \u017eupanija')),
)

"""
Sources:
http://hr.wikipedia.org/wiki/Dodatak:Popis_registracijskih_oznaka_za_cestovna_vozila_u_Hrvatskoj

Only common license plate prefixes are provided. Special cases and obsolete prefixes are omitted.
"""

HR_LICENSE_PLATE_PREFIX_CHOICES = (
    ('BJ', 'BJ'),
    ('BM', 'BM'),
    ('\u010cK', '\u010cK'),
    ('DA', 'DA'),
    ('DE', 'DE'),
    ('DJ', 'DJ'),
    ('DU', 'DU'),
    ('GS', 'GS'),
    ('IM', 'IM'),
    ('KA', 'KA'),
    ('KC', 'KC'),
    ('KR', 'KR'),
    ('KT', 'KT'),
    ('K\u017d', 'K\u017d'),
    ('MA', 'MA'),
    ('NA', 'NA'),
    ('NG', 'NG'),
    ('OG', 'OG'),
    ('OS', 'OS'),
    ('PU', 'PU'),
    ('P\u017d', 'P\u017d'),
    ('RI', 'RI'),
    ('SB', 'SB'),
    ('SK', 'SK'),
    ('SL', 'SL'),
    ('ST', 'ST'),
    ('\u0160I', '\u0160I'),
    ('VK', 'VK'),
    ('VT', 'VT'),
    ('VU', 'VU'),
    ('V\u017d', 'V\u017d'),
    ('ZD', 'ZD'),
    ('ZG', 'ZG'),
    ('\u017dU', '\u017dU'),
)

"""
The list includes county and cellular network phone number prefixes.
"""

HR_PHONE_NUMBER_PREFIX_CHOICES = (
    ('1', '01'),
    ('20', '020'),
    ('21', '021'),
    ('22', '022'),
    ('23', '023'),
    ('31', '031'),
    ('32', '032'),
    ('33', '033'),
    ('34', '034'),
    ('35', '035'),
    ('40', '040'),
    ('42', '042'),
    ('43', '043'),
    ('44', '044'),
    ('47', '047'),
    ('48', '048'),
    ('49', '049'),
    ('51', '051'),
    ('52', '052'),
    ('53', '053'),
    ('91', '091'),
    ('92', '092'),
    ('95', '095'),
    ('97', '097'),
    ('98', '098'),
    ('99', '099'),
)
