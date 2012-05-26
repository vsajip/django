"""
Serialize data to/from JSON
"""

# Avoid shadowing the standard library json module
from __future__ import absolute_import

import datetime
import decimal
import json

from django.core.serializers.base import DeserializationError
from django.core.serializers.python import Serializer as PythonSerializer
from django.core.serializers.python import Deserializer as PythonDeserializer
from django.utils.py3 import StringIO, string_types, text_type
from django.utils.timezone import is_aware

class Serializer(PythonSerializer):
    """
    Convert a queryset to JSON.
    """
    internal_use_only = False

    def start_serialization(self):
        if json.__version__.split('.') >= ['2', '1', '3']:
            # Use JS strings to represent Python Decimal instances (ticket #16850)
            self.options.update({'use_decimal': False})
        self._current = None
        self.json_kwargs = self.options.copy()
        self.json_kwargs.pop('stream', None)
        self.json_kwargs.pop('fields', None)
        self.stream.write("[")

    def end_serialization(self):
        if self.options.get("indent"):
            self.stream.write("\n")
        self.stream.write("]")
        if self.options.get("indent"):
            self.stream.write("\n")

    def end_object(self, obj):
        # self._current has the field data
        indent = self.options.get("indent")
        if not self.first:
            self.stream.write(",")
            if not indent:
                self.stream.write(" ")
        if indent:
            self.stream.write("\n")
        json.dump(self.get_dump_object(obj), self.stream,
                  cls=DjangoJSONEncoder, **self.json_kwargs)
        self._current = None

    def getvalue(self):
        # overwrite PythonSerializer.getvalue() with base Serializer.getvalue()
        if callable(getattr(self.stream, 'getvalue', None)):
            return self.stream.getvalue()


def Deserializer(stream_or_string, **options):
    """
    Deserialize a stream or string of JSON data.
    """
    # django3: This code has been rejigged because binary data
    # needs more careful handling on Python 3.x. Since both
    # on 2.6+ and 3.x, json.load calls json.loads internally
    # anyway, we don't need to worry about saving memory: just
    # read all the data here and if binary, decode it using
    # utf-8.
    # simplejson might have worked differently, but that's
    # neither here nor there.
    if isinstance(stream_or_string, string_types):
        string = stream_or_string
    else:
        string = stream_or_string.read()
        if not isinstance(string, text_type):
            string = string.decode('utf-8')
    try:
        for obj in PythonDeserializer(json.loads(string), **options):
            yield obj
    except GeneratorExit:
        raise
    except Exception as e:
        # Map to deserializer error
        raise DeserializationError(e)


class DjangoJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time and decimal types.
    """
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, decimal.Decimal):
            return str(o)
        else:
            return super(DjangoJSONEncoder, self).default(o)

# Older, deprecated class name (for backwards compatibility purposes).
DateTimeAwareJSONEncoder = DjangoJSONEncoder

