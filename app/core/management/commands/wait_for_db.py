# sleep for a few seconds in between each database check.
import time
#  use to test if the database connection is available.
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
# create custom command


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        # he handle function is what is ran whenever we run this
        # management command.
        # *args, **options: for customizing the wait time, but we'll keep
        # it simple check if the databases available and then once
        # it's available we're going to cleanly exit
        """Handle the command"""
        self.stdout.write('Waiting for database...')
        # output a message to the screen
        db_conn = None
        # data base connection
        while not db_conn:
            try:
                db_conn = connections['default']
                # try and set db.conn to the database connection
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

            # continue this process until the database is finally available in
            # which case this code won't be called and it will just exit.

        self.stdout.write(self.style.SUCCESS('Database available!'))
        # communicates to the user that this was ran successfully and that the
        # database is successful


# because we mocked the time.sleep in our test function it didn't
# actually wait the time which is fine because as we explained
# previously we don't want these extra delays holding up the test
# execution but when we run it in practice it should sleep for
# a second in between each try.
