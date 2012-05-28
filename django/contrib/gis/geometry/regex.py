import re

# Regular expression for recognizing HEXEWKB and WKT.  A prophylactic measure
# to prevent potentially malicious input from reaching the underlying C
# library.  Not a substitute for good Web security programming practices.
hex_regex = re.compile(br'^[0-9A-F]+$', re.I)
wkt_regex = re.compile(br'^(SRID=(?P<srid>\-?\d+);)?'
                       br'(?P<wkt>'
                       br'(?P<type>POINT|LINESTRING|LINEARRING|POLYGON|MULTIPOINT|MULTILINESTRING|MULTIPOLYGON|GEOMETRYCOLLECTION)'
                       br'[ACEGIMLONPSRUTYZ\d,\.\-\(\) ]+)$',
                       re.I)
json_regex = re.compile(br'^(\s+)?\{[\s\w,\[\]\{\}\-\."\':]+\}(\s+)?$')
