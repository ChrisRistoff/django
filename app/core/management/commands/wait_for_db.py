# django command to wait for db to be ready before running migrations
# and starting the server
# this is a workaround for the issue with docker-compose

import time
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):

    # *args allows us to pass any number of arguments
    # **options allows us to pass any number of keyword arguments
    # we use them to make the command reusable and configurable
    def handle(self, *args, **options):

        # wait for db to be ready before running migrations
        # and starting the server
        self.stdout.write('Waiting for db...')
        # db_up is a flag to check if the db is ready or not
        # we set it to False at the beginning and then we check
        db_up = False

        # we will loop until the db is ready and then we will exit
        while not db_up:
            try:
                # we call the check method of the Command class
                # this method is inherited from BaseCommand class
                # and it will check if the db is ready or not
                self.check(databases=['default'])
                # if the db is ready we set the flag to True and exit the loop
                db_up = True

            # if the db is not ready we will catch the error and wait 1 second
            # then we will try again
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Db not ready, waiting 1 second...')
                time.sleep(1)

        # if the db is ready we will print a message to the console and exit
        self.stdout.write(self.style.SUCCESS('Db is ready!'))
