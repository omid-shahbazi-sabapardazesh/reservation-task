import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        db_conn = None
        start_time = time.time()
        while not db_conn:
            try:
                db_conn = connections['default']
                c = db_conn.cursor()
            except OperationalError:
                if time.time() - start_time > 30:
                    raise Exception("cannot connect to DB")
                time.sleep(1)
