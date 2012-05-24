# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template import Template, TemplateEncodingError, Context
from django.utils.safestring import SafeData
from django.utils.unittest import TestCase
from django.utils.py3 import text_type

class UnicodeTests(TestCase):
    def test_template(self):
        # Templates can be created from unicode strings.
        t1 = Template('\u0160\u0110\u0106\u017d\u0107\u017e\u0161\u0111 {{ var }}')
        # Templates can also be created from bytestrings. These are assumed to
        # be encoded using UTF-8.
        s = b'\xc5\xa0\xc4\x90\xc4\x86\xc5\xbd\xc4\x87\xc5\xbe\xc5\xa1\xc4\x91 {{ var }}'
        t2 = Template(s)
        s = b'\x80\xc5\xc0'
        self.assertRaises(TemplateEncodingError, Template, s)

        # Contexts can be constructed from unicode or UTF-8 bytestrings.
        c1 = Context({"var": "foo"})
        c2 = Context({"var": "foo"})
        c3 = Context({"var": "\u0110\u0111"})
        c4 = Context({"var": "\xc4\x90\xc4\x91"})

        # Since both templates and all four contexts represent the same thing,
        # they all render the same (and are returned as unicode objects and
        # "safe" objects as well, for auto-escaping purposes).
        self.assertEqual(t1.render(c3), t2.render(c3))
        self.assertIsInstance(t1.render(c3), text_type)
        self.assertIsInstance(t1.render(c3), SafeData)
