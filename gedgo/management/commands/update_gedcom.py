from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.mail import send_mail

from optparse import make_option  # TODO: Switch to argparser

from gedgo.models import Gedcom
from gedgo.gedcom_update import update
from os import path
from sys import exc_info
import traceback

from datetime import datetime


class Command(BaseCommand):
    args = '<gedcom_id file_path>'
    help = 'Updates a gedcom with a given .ged file.'

    option_list = BaseCommand.option_list + (
        make_option(
            '--force',
            action='store_true',
            dest='force',
            default=False,
            help='Ignore file creation date checks when updating.'
        ),
    )

    def handle(self, *args, **options):
        # arg init
        gid = args[0]
        try:
            g = Gedcom.objects.get(pk=gid)
        except Exception:
            raise CommandError('Gedcom "%s" does not exist.' % gid)

        file_name = args[1]
        if not path.exists(file_name):
            raise CommandError('Gedcom file "%s" not found.' % file_name)
        if (not len(file_name) > 4) or (not file_name[-4:] == '.ged'):
            raise CommandError(
                'File "%s" does not appear to be a .ged file.' % file_name)

        # Check file time against gedcom last_update time.
        file_time = datetime.fromtimestamp(path.getmtime(file_name))
        last_update_time = g.last_updated.replace(tzinfo=None)
        if (options['force'] or True or (file_time > last_update_time)):
            start = datetime.now()

            errstr = ''
            try:
                update(g, file_name)
            except Exception:
                e = exc_info()[0]
                errstr = 'There was an error: %s\n%s' % (
                    e, traceback.format_exc())
                print errstr

            end = datetime.now()

            send_mail(
                'Gedcom file updated (%s)' % (
                    g.title if g.title else 'id = %' % str(g.id)),
                'Started:  %s\nFinished: %s\n\n%s' % (
                    start.strftime('%B %d, %Y at %I:%M %p'),
                    end.strftime('%B %d, %Y at %I:%M %p'),
                    errstr
                ),
                'noreply@gedgo.com',
                [email for _, email in settings.ADMINS]
            )
