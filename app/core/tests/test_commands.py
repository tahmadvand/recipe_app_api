# first thing we're going to import is the patch
# function from the unit tests.mock module.
# This is going to allow us to mock the
# behavior of the Django get database function.

from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
# when db is not available
from django.test import TestCase


class CommandsTestCase(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""

        # we're gonna mock the behavior
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            # return this value that we specify here and the second thing
            # is it allows us to monitor how many times it was called and
            # the different calls that were made to it
            call_command('wait_for_db')
            # wait_for_db is the name of management command
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    # mock the time.sleep, speed up the test
    def test_wait_for_db(self, ts):
        """Test waiting for db"""

        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            #  the first five times you call this get item it's going to
            #  raise the operational error.
            # then on the sixth time it won't raise the error it will
            # just return.
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
            # call this function for 6 times
