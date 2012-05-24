from __future__ import unicode_literals

import os
from optparse import make_option
from django.core.management.base import LabelCommand
from django.utils.encoding import smart_str, smart_unicode, smart_text
from django.utils.py3 import PY3
from django.contrib.staticfiles import finders

class Command(LabelCommand):
    help = "Finds the absolute paths for the given static file(s)."
    args = "[file ...]"
    label = 'static file'
    option_list = LabelCommand.option_list + (
        make_option('--first', action='store_false', dest='all', default=True,
                    help="Only return the first match for each static file."),
    )

    def handle_label(self, path, **options):
        verbosity = int(options.get('verbosity', 1))
        result = finders.find(path, all=options['all'])
        path = smart_unicode(path)
        if result:
            if not isinstance(result, (list, tuple)):
                result = [result]
            output = '\n  '.join(
                (smart_unicode(os.path.realpath(path)) for path in result))
            s = smart_text("Found '%s' here:\n  %s" % (path, output))
            self.stdout.write(s)
        else:
            if verbosity >= 1:
                self.stderr.write("No matching file found for '%s'." % path)
