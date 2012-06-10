from __future__ import unicode_literals

import copy
import pickle

from django.http import (QueryDict, HttpResponse, SimpleCookie, BadHeaderError,
        parse_cookie)
from django.utils import unittest
from django.utils.py3 import (unichr, next, PY3, n,
                              dictitems, dictkeys, dictvalues)

class QueryDictTests(unittest.TestCase):
    def test_missing_key(self):
        q = QueryDict('')
        self.assertRaises(KeyError, q.__getitem__, 'foo')

    def test_immutability(self):
        q = QueryDict('')
        self.assertRaises(AttributeError, q.__setitem__, 'something', 'bar')
        self.assertRaises(AttributeError, q.setlist, 'foo', ['bar'])
        self.assertRaises(AttributeError, q.appendlist, 'foo', ['bar'])
        self.assertRaises(AttributeError, q.update, {'foo': 'bar'})
        self.assertRaises(AttributeError, q.pop, 'foo')
        self.assertRaises(AttributeError, q.popitem)
        self.assertRaises(AttributeError, q.clear)

    def test_immutable_get_with_default(self):
        q = QueryDict('')
        self.assertEqual(q.get('foo', 'default'), 'default')

    def test_immutable_basic_operations(self):
        q = QueryDict('')
        self.assertEqual(q.getlist('foo'), [])
        if not PY3:
            self.assertEqual(q.has_key('foo'), False)
        self.assertEqual('foo' in q, False)
        self.assertEqual(dictitems(q), [])
        self.assertEqual(q.lists(), [])
        self.assertEqual(dictitems(q), [])
        self.assertEqual(dictkeys(q), [])
        self.assertEqual(dictvalues(q), [])
        self.assertEqual(len(q), 0)
        self.assertEqual(q.urlencode(), '')

    def test_single_key_value(self):
        """Test QueryDict with one key/value pair"""

        q = QueryDict('foo=bar')
        self.assertEqual(q['foo'], 'bar')
        self.assertRaises(KeyError, q.__getitem__, 'bar')
        self.assertRaises(AttributeError, q.__setitem__, 'something', 'bar')

        self.assertEqual(q.get('foo', 'default'), 'bar')
        self.assertEqual(q.get('bar', 'default'), 'default')
        self.assertEqual(q.getlist('foo'), ['bar'])
        self.assertEqual(q.getlist('bar'), [])

        self.assertRaises(AttributeError, q.setlist, 'foo', ['bar'])
        self.assertRaises(AttributeError, q.appendlist, 'foo', ['bar'])

        if not PY3:
            self.assertTrue(q.has_key('foo'))
        self.assertTrue('foo' in q)
        if not PY3:
            self.assertFalse(q.has_key('bar'))
        self.assertFalse('bar' in q)

        self.assertEqual(dictitems(q), [('foo', 'bar')])
        self.assertEqual(q.lists(), [('foo', ['bar'])])
        self.assertEqual(dictkeys(q), ['foo'])
        self.assertEqual(dictvalues(q), ['bar'])
        self.assertEqual(len(q), 1)

        self.assertRaises(AttributeError, q.update, {'foo': 'bar'})
        self.assertRaises(AttributeError, q.pop, 'foo')
        self.assertRaises(AttributeError, q.popitem)
        self.assertRaises(AttributeError, q.clear)
        self.assertRaises(AttributeError, q.setdefault, 'foo', 'bar')

        self.assertEqual(q.urlencode(), 'foo=bar')

    def test_urlencode(self):
        q = QueryDict('', mutable=True)
        q['next'] = '/a&b/'
        self.assertEqual(q.urlencode(), 'next=%2Fa%26b%2F')
        self.assertEqual(q.urlencode(safe='/'), 'next=/a%26b/')
        q = QueryDict('', mutable=True)
        q['next'] = '/t\xebst&key/'
        self.assertEqual(q.urlencode(), 'next=%2Ft%C3%ABst%26key%2F')
        self.assertEqual(q.urlencode(safe='/'), 'next=/t%C3%ABst%26key/')

    def test_mutable_copy(self):
        """A copy of a QueryDict is mutable."""
        q = QueryDict('').copy()
        self.assertRaises(KeyError, q.__getitem__, "foo")
        q['name'] = 'john'
        self.assertEqual(q['name'], 'john')

    def test_mutable_delete(self):
        q = QueryDict('').copy()
        q['name'] = 'john'
        del q['name']
        self.assertFalse('name' in q)

    def test_basic_mutable_operations(self):
        q = QueryDict('').copy()
        q['name'] = 'john'
        self.assertEqual(q.get('foo', 'default'), 'default')
        self.assertEqual(q.get('name', 'default'), 'john')
        self.assertEqual(q.getlist('name'), ['john'])
        self.assertEqual(q.getlist('foo'), [])

        q.setlist('foo', ['bar', 'baz'])
        self.assertEqual(q.get('foo', 'default'), 'baz')
        self.assertEqual(q.getlist('foo'), ['bar', 'baz'])

        q.appendlist('foo', 'another')
        self.assertEqual(q.getlist('foo'), ['bar', 'baz', 'another'])
        self.assertEqual(q['foo'], 'another')
        if not PY3:
            self.assertTrue(q.has_key('foo'))
        self.assertTrue('foo' in q)

        self.assertEqual(dictitems(q),  [('foo', 'another'), ('name', 'john')])
        self.assertEqual(q.lists(), [('foo', ['bar', 'baz', 'another']), ('name', ['john'])])
        self.assertEqual(dictkeys(q), ['foo', 'name'])
        self.assertEqual(dictvalues(q), ['another', 'john'])
        self.assertEqual(len(q), 2)

        q.update({'foo': 'hello'})
        self.assertEqual(q['foo'], 'hello')
        self.assertEqual(q.get('foo', 'not available'), 'hello')
        self.assertEqual(q.getlist('foo'), ['bar', 'baz', 'another', 'hello'])
        self.assertEqual(q.pop('foo'), ['bar', 'baz', 'another', 'hello'])
        self.assertEqual(q.pop('foo', 'not there'), 'not there')
        self.assertEqual(q.get('foo', 'not there'), 'not there')
        self.assertEqual(q.setdefault('foo', 'bar'), 'bar')
        self.assertEqual(q['foo'], 'bar')
        self.assertEqual(q.getlist('foo'), ['bar'])
        self.assertEqual(q.urlencode(), 'foo=bar&name=john')

        q.clear()
        self.assertEqual(len(q), 0)

    def test_multiple_keys(self):
        """Test QueryDict with two key/value pairs with same keys."""

        q = QueryDict('vote=yes&vote=no')

        self.assertEqual(q['vote'], 'no')
        self.assertRaises(AttributeError, q.__setitem__, 'something', 'bar')

        self.assertEqual(q.get('vote', 'default'), 'no')
        self.assertEqual(q.get('foo', 'default'), 'default')
        self.assertEqual(q.getlist('vote'), ['yes', 'no'])
        self.assertEqual(q.getlist('foo'), [])

        self.assertRaises(AttributeError, q.setlist, 'foo', ['bar', 'baz'])
        self.assertRaises(AttributeError, q.setlist, 'foo', ['bar', 'baz'])
        self.assertRaises(AttributeError, q.appendlist, 'foo', ['bar'])

        if not PY3:
            self.assertEqual(q.has_key('vote'), True)
        self.assertEqual('vote' in q, True)
        if not PY3:
            self.assertEqual(q.has_key('foo'), False)
        self.assertEqual('foo' in q, False)
        self.assertEqual(dictitems(q), [('vote', 'no')])
        self.assertEqual(q.lists(), [('vote', ['yes', 'no'])])
        self.assertEqual(dictkeys(q), ['vote'])
        self.assertEqual(dictvalues(q), ['no'])
        self.assertEqual(len(q), 1)

        self.assertRaises(AttributeError, q.update, {'foo': 'bar'})
        self.assertRaises(AttributeError, q.pop, 'foo')
        self.assertRaises(AttributeError, q.popitem)
        self.assertRaises(AttributeError, q.clear)
        self.assertRaises(AttributeError, q.setdefault, 'foo', 'bar')
        self.assertRaises(AttributeError, q.__delitem__, 'vote')

    @unittest.skipIf(PY3, 'django3: Invalid encoding handling differs between 2.x and 3.x.')
    def test_invalid_input_encoding(self):
        """
        QueryDicts must be able to handle invalid input encoding (in this
        case, bad UTF-8 encoding).
        """
        q = QueryDict(b'foo=bar&foo=\xff')
        self.assertEqual(q['foo'], '\ufffd')
        self.assertEqual(q.getlist('foo'), ['bar', '\ufffd'])

    def test_pickle(self):
        q = QueryDict('')
        q1 = pickle.loads(pickle.dumps(q, 2))
        self.assertEqual(q == q1, True)
        q = QueryDict('a=b&c=d')
        q1 = pickle.loads(pickle.dumps(q, 2))
        self.assertEqual(q == q1, True)
        q = QueryDict('a=b&c=d&a=1')
        q1 = pickle.loads(pickle.dumps(q, 2))
        self.assertEqual(q == q1 , True)

    def test_update_from_querydict(self):
        """Regression test for #8278: QueryDict.update(QueryDict)"""
        x = QueryDict("a=1&a=2", mutable=True)
        y = QueryDict("a=3&a=4")
        x.update(y)
        self.assertEqual(x.getlist('a'), ['1', '2', '3', '4'])

    @unittest.skipIf(PY3, 'django3: rot-13 encoding is not straightforward on Python 3.x.')
    def test_non_default_encoding(self):
        """#13572 - QueryDict with a non-default encoding"""
        ENCODING = 'rot_13'
        q = QueryDict(n('sbb=one'), encoding=ENCODING)
        self.assertEqual(q.encoding , ENCODING)
        self.assertEqual(dictitems(q) , [('foo', 'bar')])
        self.assertEqual(q.urlencode() , 'sbb=one')
        q = q.copy()
        self.assertEqual(q.encoding, ENCODING)
        self.assertEqual(dictitems(q) , [('foo', 'bar')])
        self.assertEqual(q.urlencode(), 'sbb=one')
        self.assertEqual(copy.copy(q).encoding, ENCODING)
        self.assertEqual(copy.deepcopy(q).encoding , ENCODING)

class HttpResponseTests(unittest.TestCase):
    def test_unicode_headers(self):
        r = HttpResponse()

        # If we insert a unicode value it will be converted to an ascii
        r['value'] = 'test value'
        self.assertTrue(isinstance(r['value'], str))

        # An error is raised when a unicode object with non-ascii is assigned.
        self.assertRaises(UnicodeEncodeError, r.__setitem__, 'value', 't\xebst value')

        # An error is raised when  a unicode object with non-ASCII format is
        # passed as initial mimetype or content_type.
        self.assertRaises(UnicodeEncodeError, HttpResponse,
                content_type='t\xebst value')

        # HttpResponse headers must be convertible to ASCII.
        self.assertRaises(UnicodeEncodeError, HttpResponse,
                content_type='t\xebst value')

        # The response also converts unicode keys to strings.)
        r['test'] = 'testing key'
        l = sorted(r.items())
        self.assertEqual(l[1], ('test', 'testing key'))

        # It will also raise errors for keys with non-ascii data.
        self.assertRaises(UnicodeEncodeError, r.__setitem__, 't\xebst key', 'value')

    def test_newlines_in_headers(self):
        # Bug #10188: Do not allow newlines in headers (CR or LF)
        r = HttpResponse()
        self.assertRaises(BadHeaderError, r.__setitem__, 'test\rstr', 'test')
        self.assertRaises(BadHeaderError, r.__setitem__, 'test\nstr', 'test')

    def test_dict_behavior(self):
        """
        Test for bug #14020: Make HttpResponse.get work like dict.get
        """
        r = HttpResponse()
        self.assertEqual(r.get('test'), None)

    def test_non_string_content(self):
        #Bug 16494: HttpResponse should behave consistently with non-strings
        r = HttpResponse(12345)
        self.assertEqual(r.content, b'12345')

        #test content via property
        r = HttpResponse()
        r.content = 12345
        self.assertEqual(r.content, b'12345')

    def test_iter_content(self):
        r = HttpResponse(['abc', 'def', 'ghi'])
        self.assertEqual(r.content, b'abcdefghi')

        #test iter content via property
        r = HttpResponse()
        r.content = ['idan', 'alex', 'jacob']
        self.assertEqual(r.content, b'idanalexjacob')

        r = HttpResponse()
        r.content = [1, 2, 3]
        self.assertEqual(r.content, b'123')

        #test retrieval explicitly using iter and odd inputs
        r = HttpResponse()
        r.content = ['1', '2', 3, unichr(1950)]
        result = []
        my_iter = r.__iter__()
        while True:
            try:
                result.append(next(my_iter))
            except StopIteration:
                break
        #'\xde\x9e' == unichr(1950).encode('utf-8')
        self.assertEqual(result, [b'1', b'2', b'3', b'\xde\x9e'])
        self.assertEqual(r.content, b'123\xde\x9e')

        #with Content-Encoding header
        r = HttpResponse([1,1,2,4,8])
        r['Content-Encoding'] = 'winning'
        self.assertEqual(r.content, b'11248')
        # django3: The following checks has changed,
        # since we have changed the handling of iterated content
        r.content = [unichr(1950),]
        #self.assertRaises(UnicodeEncodeError,
        #                  getattr, r, 'content')
        self.assertEqual(r.content, b'\xde\x9e')

class CookieTests(unittest.TestCase):
    def test_encode(self):
        """
        Test that we don't output tricky characters in encoded value
        """
        c = SimpleCookie()
        c[n('test')] = "An,awkward;value"
        self.assertTrue(";" not in c.output().rstrip(';')) # IE compat
        self.assertTrue("," not in c.output().rstrip(';')) # Safari compat

    def test_decode(self):
        """
        Test that we can still preserve semi-colons and commas
        """
        c = SimpleCookie()
        c[n('test')] = "An,awkward;value"
        c2 = SimpleCookie()
        c2.load(n(c.output()))
        self.assertEqual(c['test'].value, c2['test'].value)

    def test_decode_2(self):
        """
        Test that we haven't broken normal encoding
        """
        c = SimpleCookie()
        c[n('test')] = n("\xf0")
        c2 = SimpleCookie()
        c2.load(n(c.output()))
        self.assertEqual(c['test'].value, c2['test'].value)

    def test_nonstandard_keys(self):
        """
        Test that a single non-standard cookie name doesn't affect all cookies. Ticket #13007.
        """
        self.assertTrue('good_cookie' in parse_cookie('good_cookie=yes;bad:cookie=yes').keys())

    def test_repeated_nonstandard_keys(self):
        """
        Test that a repeated non-standard name doesn't affect all cookies. Ticket #15852
        """
        self.assertTrue('good_cookie' in parse_cookie('a,=b; a,=c; good_cookie=yes').keys())

    def test_httponly_after_load(self):
        """
        Test that we can use httponly attribute on cookies that we load
        """
        c = SimpleCookie()
        c.load(n("name=val"))
        c['name']['httponly'] = True
        self.assertTrue(c['name']['httponly'])

