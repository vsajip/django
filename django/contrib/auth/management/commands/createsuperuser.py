"""
Management utility to create superusers.
"""

import getpass
import re
import sys
from optparse import make_option

from django.contrib.auth.models import User
from django.contrib.auth.management import get_default_username
from django.core import exceptions
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS
from django.utils import six
from django.utils.translation import ugettext as _

RE_VALID_USERNAME = re.compile('[\w.@+-]+$')

EMAIL_RE = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)  # domain


def is_valid_email(value):
    if not EMAIL_RE.search(value):
        raise exceptions.ValidationError(_('Enter a valid e-mail address.'))


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--username', dest='username', default=None,
            help='Specifies the username for the superuser.'),
        make_option('--email', dest='email', default=None,
            help='Specifies the email address for the superuser.'),
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help=('Tells Django to NOT prompt the user for input of any kind. '
                  'You must use --username and --email with --noinput, and '
                  'superusers created with --noinput will not be able to log '
                  'in until they\'re given a valid password.')),
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Specifies the database to use. Default is "default".'),
    )
    help = 'Used to create a superuser.'

    def handle(self, *args, **options):
        username = options.get('username', None)
        email = options.get('email', None)
        interactive = options.get('interactive')
        verbosity = int(options.get('verbosity', 1))
        database = options.get('database')

        # Do quick and dirty validation if --noinput
        if not interactive:
            if not username or not email:
                raise CommandError("You must use --username and --email with --noinput.")
            if not RE_VALID_USERNAME.match(username):
                raise CommandError("Invalid username. Use only letters, digits, and underscores")
            try:
                is_valid_email(email)
            except exceptions.ValidationError:
                raise CommandError("Invalid email address.")

        # If not provided, create the user with an unusable password
        password = None

        # Prompt for username/email/password. Enclose this whole thing in a
        # try/except to trap for a keyboard interrupt and exit gracefully.
        if interactive:
            default_username = get_default_username()
            try:

                # Get a username
                while 1:
                    if not username:
                        input_msg = 'Username'
                        if default_username:
                            input_msg += ' (leave blank to use %r)' % default_username
                        username = six.raw_input(input_msg + ': ')
                    if default_username and username == '':
                        username = default_username
                    if not RE_VALID_USERNAME.match(username):
                        self.stderr.write("Error: That username is invalid. Use only letters, digits and underscores.")
                        username = None
                        continue
                    try:
                        User.objects.using(database).get(username=username)
                    except User.DoesNotExist:
                        break
                    else:
                        self.stderr.write("Error: That username is already taken.")
                        username = None

                # Get an email
                while 1:
                    if not email:
                        email = six.raw_input('E-mail address: ')
                    try:
                        is_valid_email(email)
                    except exceptions.ValidationError:
                        self.stderr.write("Error: That e-mail address is invalid.")
                        email = None
                    else:
                        break

                # Get a password
                while 1:
                    if not password:
                        password = getpass.getpass()
                        password2 = getpass.getpass('Password (again): ')
                        if password != password2:
                            self.stderr.write("Error: Your passwords didn't match.")
                            password = None
                            continue
                    if password.strip() == '':
                        self.stderr.write("Error: Blank passwords aren't allowed.")
                        password = None
                        continue
                    break
            except KeyboardInterrupt:
                self.stderr.write("\nOperation cancelled.")
                sys.exit(1)

        User.objects.db_manager(database).create_superuser(username, email, password)
        if verbosity >= 1:
          self.stdout.write("Superuser created successfully.")

