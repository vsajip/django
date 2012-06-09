# Compatibility layer for running Django both in 2.x and 3.x
"""
This module currently provides the following helper symbols
 * bytes (name of byte string type; str in 2.x, bytes in 3.x)
 * b (function converting a string literal to an ASCII byte string;
      can be also used to convert a Unicode string with only ASCII
      characters into a byte string)
 * byte (data type for an individual byte)
 * dictvalues returns the .values() of a dict as a list.
   There is a 2to3 fixer for this, but it conflicts with the .values()
   method in django.db.
"""
import sys

if sys.version_info[0] < 3:
    PY3 = False
    import __builtin__ as builtins
    b = bytes = str
    def byte(n):
        return n
    def u(s):
        if not isinstance(s, unicode):
            s = unicode(s, "unicode_escape")
        return s

    def next(i):
        return i.next()
    nextname = 'next'
    dictkeys = lambda d: d.keys()
    dictvalues = lambda d: d.values()
    dictitems = lambda d: d.items()
    lrange = range
    lzip = zip
    lmap = map
    lfilter = filter
    string_types = basestring,
    text_type = unicode
    binary_type = str
    integer_types = int, long
    long_type = long
    items = lambda o: o.items
    iteritems = lambda o: o.iteritems()
    itervalues = lambda o: o.itervalues()
    iterkeys = lambda o: o.iterkeys()
    def with_metaclass(meta, base=object):
        class _DjangoBase(base):
            __metaclass__ = meta
        return _DjangoBase
    reduce = reduce
    raw_input = raw_input
    from urlparse import (urlparse, urlunparse, urljoin, urlsplit, urlunsplit,
                          urldefrag)
    from urllib import (quote, unquote, quote_plus, urlopen, urlencode,
                        url2pathname, urlretrieve, unquote_plus)
    from urllib2 import (Request, OpenerDirector, UnknownHandler, HTTPHandler,
                         HTTPSHandler, HTTPDefaultErrorHandler, FTPHandler,
                         HTTPErrorProcessor)
    try:
        from urlparse import parse_qsl
    except ImportError:
        from cgi import parse_qsl
    from StringIO import StringIO as PyStringIO
    try:
        from cStringIO import StringIO
    except ImportError:
        StringIO = PyStringIO
    BytesIO = StringIO
    try:
        import cPickle as pickle
    except ImportError:
        import pickle
    from itertools import izip
    from itertools import izip_longest
    xrange = xrange
    execfile_ = execfile
    from SocketServer import ThreadingMixIn
    try:
        import thread
    except ImportError:
        import dummy_thread as thread
    def exec_(code, globs=None, locs=None):
        """Execute code in a namespace."""
        if globs is None:
            frame = sys._getframe(1)
            globs = frame.f_globals
            if locs is None:
                locs = frame.f_locals
            del frame
        elif locs is None:
            locs = globs
        exec("""exec code in globs, locs""")
    exec_("""def reraise(tp, value, tb=None):
    raise tp, value, tb
""")
    import Cookie as cookies
    from os import getcwdu
    maxsize = sys.maxint
    next_name = 'next'
    from htmlentitydefs import name2codepoint
    unichr = unichr
    def fromhex(s):
        return s.decode('hex')
    import urllib2
    upfx = 'u'
    n = lambda s: s.encode('utf-8')
    from HTMLParser import HTMLParseError
    import HTMLParser
else:
    PY3 = True
    import builtins
    bytes = builtins.bytes
    def b(s):
        if isinstance(s, str):
            try:
                return s.encode("latin-1")
            except UnicodeEncodeError:
                return s.encode("utf-8")
        elif isinstance(s, bytes):
            return s
        else:
            raise TypeError("Invalid argument %r for b()" % (s,))
    def byte(n):
        # assume n is a Latin-1 string of length 1
        return ord(n)
    def u(s):
        return s.replace('\\\\', '\\')
    next = builtins.next
    nextname = '__next__'
    dictkeys = lambda d: list(d.keys())
    dictvalues = lambda d: list(d.values())
    dictitems = lambda d: list(d.items())
    lrange = lambda *args: list(range(*args))
    lzip = lambda *args: list(zip(*args))
    lmap = lambda *args: list(map(*args))
    lfilter = lambda *args: list(filter(*args))
    string_types = str,
    text_type = str
    binary_type = bytes
    integer_types = int,
    long_type = int
    items = lambda o: list(o.items)
    iteritems = lambda o: o.items()
    itervalues = lambda o: o.values()
    iterkeys = lambda o: o.keys()
    exec_ = getattr(builtins, 'exec')
    def with_metaclass(meta, base=object):
        ns = dict(base=base, meta=meta)
        exec_("""class _DjangoBase(base, metaclass=meta):
    pass""", ns)
        return ns["_DjangoBase"]
    from functools import reduce
    raw_input = input
    from urllib.parse import (urlparse, urlunparse, urlencode, urljoin,
                              urlsplit, urlunsplit, quote, unquote,
                              quote_plus, unquote_plus, parse_qsl,
                              urldefrag)
    from urllib.request import (urlopen, url2pathname, Request, OpenerDirector,
                                UnknownHandler, HTTPHandler, HTTPSHandler,
                                HTTPDefaultErrorHandler, FTPHandler,
                                HTTPErrorProcessor, urlretrieve)
    from io import StringIO, BytesIO
    PyStringIO = StringIO
    import pickle
    izip = zip
    from itertools import zip_longest as izip_longest
    xrange = range
    def execfile_(file, globals=globals(), locals=locals()):
        f = open(file, "r")
        try:
            exec_(f.read()+"\\n", globals, locals)
        finally:
            f.close()
    from socketserver import ThreadingMixIn
    try:
        import _thread as thread
    except ImportError:
        import _dummy_thread as thread
    def reraise(tp, value, tb=None):
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value
    import http.cookies as cookies
    from os import getcwd as getcwdu
    maxsize = sys.maxsize
    next_name = '__next__'
    from html.entities import name2codepoint
    unichr = chr
    def fromhex(s):
        return bytes.fromhex(s)
    import urllib.request as urllib2
    upfx = ''
    n = lambda s: s
    from html.parser import HTMLParseError
    import html.parser as HTMLParser
    
def py3_prefix(s):
    return s % { '_': upfx }
