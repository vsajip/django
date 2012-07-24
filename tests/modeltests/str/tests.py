 # -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import datetime

from django.test import TestCase
from django.utils import six

from .models import Article, InternationalArticle


class SimpleTests(TestCase):
    def test_basic(self):
        a = Article.objects.create(
            headline='Area man programs in Python',
            pub_date=datetime.datetime(2005, 7, 28)
        )
        self.assertEqual(str(a), 'Area man programs in Python')
        self.assertEqual(repr(a), '<Article: Area man programs in Python>')

    def test_international(self):
        a = InternationalArticle.objects.create(
            headline='Girl wins €12.500 in lottery',
            pub_date=datetime.datetime(2005, 7, 28)
        )
        # The default str() output will be the UTF-8 encoded output of __unicode__().
        # django3: Above comment applies to 2.x. On 3.x, we get the Unicode string.
        s = str(a)
        if six.PY3: s = s.encode('utf-8')
        self.assertEqual(s, b'Girl wins \xe2\x82\xac12.500 in lottery')
