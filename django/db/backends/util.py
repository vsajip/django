from __future__ import unicode_literals

import datetime
import decimal
import hashlib
from time import time

from django.conf import settings
from django.utils.log import getLogger
from django.utils import six
from django.utils.timezone import utc


logger = getLogger('django.db.backends')


class CursorWrapper(object):
    def __init__(self, cursor, db):
        self.cursor = cursor
        self.db = db

    def set_dirty(self):
        if self.db.is_managed():
            self.db.set_dirty()

    def __getattr__(self, attr):
        self.set_dirty()
        if attr in self.__dict__:
            return self.__dict__[attr]
        else:
            return getattr(self.cursor, attr)

    def __iter__(self):
        return iter(self.cursor)


class CursorDebugWrapper(CursorWrapper):

    def execute(self, sql, params=()):
        self.set_dirty()
        start = time()
        try:
            return self.cursor.execute(sql, params)
        finally:
            stop = time()
            duration = stop - start
            sql = self.db.ops.last_executed_query(self.cursor, sql, params)
            self.db.queries.append({
                'sql': sql,
                'time': "%.3f" % duration,
            })
            logger.debug(six.n('(%.3f) %s; args=%s') % (duration, sql, params),
                extra={six.n('duration'):duration, six.n('sql'): sql, six.n('params'): params}
            )

    def executemany(self, sql, param_list):
        self.set_dirty()
        start = time()
        try:
            return self.cursor.executemany(sql, param_list)
        finally:
            stop = time()
            duration = stop - start
            try:
                times = len(param_list)
            except TypeError:           # param_list could be an iterator
                times = '?'
            self.db.queries.append({
                'sql': '%s times: %s' % (times, sql),
                'time': "%.3f" % duration,
            })
            logger.debug(six.n('(%.3f) %s; args=%s') % (duration, sql, param_list),
                extra={six.n('duration'): duration, six.n('sql'): sql, six.n('params'): param_list}
            )


###############################################
# Converters from a byte objects to strings #
###############################################

if six.PY3:
    def py3_string_conversion(s):
        # Convert byte s to str
        if isinstance(s, bytes):
                s = str(s, encoding='utf8')
        return s
else:
    def py3_string_conversion(s):
        return s

###############################################
# Converters from database (string) to Python #
###############################################

def typecast_date(s):
    s = py3_string_conversion(s)
    return s and datetime.date(*map(int, s.split('-'))) or None # returns None if s is null

def typecast_time(s): # does NOT store time zone information
    if not s: return None
    if isinstance(s, six.text_type): s = s.encode('utf-8')
    hour, minutes, seconds = s.split(b':')
    if b'.' in seconds: # check whether seconds have a fractional part
        seconds, microseconds = seconds.split(b'.')
    else:
        microseconds = b'0'
    return datetime.time(int(hour), int(minutes), int(seconds), int(float(b'.'+microseconds) * 1000000))

def typecast_timestamp(s): # does NOT store time zone information
    # "2005-07-29 15:48:00.590358-05"
    # "2005-07-29 09:56:00-05"
    if not s: return None
    # XXX should the database pass in Unicode here already?
    #s = s.decode("ascii")
    
    # Convert s to str anyway, granted that s is not yet a str
    s = py3_string_conversion(s)

    if not ' ' in s: return typecast_date(s)
    d, t = s.split()
    # Extract timezone information, if it exists. Currently we just throw
    # it away, but in the future we may make use of it.
    if '-' in t:
        t, tz = t.split('-', 1)
        tz = '-' + tz
    elif '+' in t:
        t, tz = t.split('+', 1)
        tz = '+' + tz
    else:
        tz = ''
    dates = d.split('-')
    times = t.split(':')
    seconds = times[2]
    if '.' in seconds: # check whether seconds have a fractional part
        seconds, microseconds = seconds.split('.')
    else:
        microseconds = '0'
    tzinfo = utc if settings.USE_TZ else None
    return datetime.datetime(int(dates[0]), int(dates[1]), int(dates[2]),
        int(times[0]), int(times[1]), int(seconds),
        int((microseconds + '000000')[:6]), tzinfo)

def typecast_decimal(s):
    s = py3_string_conversion(s)
    if s is None or s == '':
        return None
    return decimal.Decimal(s)

###############################################
# Converters from Python to database (string) #
###############################################

def rev_typecast_decimal(d):
    if d is None:
        return None
    return str(d)

def truncate_name(name, length=None, hash_len=4):
    """Shortens a string to a repeatable mangled version with the given length.
    """
    if length is None or len(name) <= length:
        return name

    hsh = hashlib.md5(name.encode('utf-8')).hexdigest()[:hash_len]
    return '%s%s' % (name[:length-hash_len], hsh)

def format_number(value, max_digits, decimal_places):
    """
    Formats a number into a string with the requisite number of digits and
    decimal places.
    """
    if isinstance(value, decimal.Decimal):
        context = decimal.getcontext().copy()
        context.prec = max_digits
        return '%s' % str(value.quantize(decimal.Decimal(".1") ** decimal_places, context=context))
    else:
        return "%.*f" % (decimal_places, value)
