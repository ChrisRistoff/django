''' test case for management commands '''

from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for db"""

        # Mock check method to return True
        patched_check.return_value = True

        # this will call the wait_for_db command and will return
        # None if the db is ready
        # if the db is not ready it will raise an error
        call_command('wait_for_db')

        # assert that the check method was called once
        # with the correct arguments
        self.assertEqual(patched_check.call_count, 1)

        # assert_called_once_with is a method of the mock object
        # it will check if the method was called once with the
        # correct arguments
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        '''Test waiting for db with delay'''

        # mock check method to return False
        # we raise the Psycopg2Error 2 times
        # then we raise the OperationalError 3 times
        # then we return True
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        # this will call the wait_for_db command and will return
        # None if the db is ready
        # if the db is not ready it will raise an error
        call_command('wait_for_db')

        # assert that the check method was called 6 times
        # with the correct arguments
        self.assertEqual(patched_check.call_count, 6)

        # assert_called_with is a method of the mock object
        # it will check if the method was called with the
        # correct arguments
        patched_check.assert_called_with(databases=['default'])
