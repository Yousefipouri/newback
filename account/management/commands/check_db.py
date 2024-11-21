import os
import pyodbc
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Checks if the database exists and creates it if it does not.'

    def handle(self, *args, **kwargs):
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_password = db_settings['PASSWORD']
        db_host = db_settings['HOST']
        db_port = db_settings.get('PORT', '1433')
        driver = db_settings['OPTIONS']['driver']

        conn_str = (
            f"DRIVER={driver};"
            f"SERVER={db_host};"
            f"DATABASE=master;"
            f"UID={db_user};"
            f"PWD={db_password}"
        )

        # Connect to the master database to check and create the target database
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            # Check if the database exists
            cursor.execute(f"SELECT * FROM sys.databases WHERE name = '{db_name}'")
            result = cursor.fetchone()

            if not result:
                self.stdout.write(f"Database {db_name} does not exist. Creating database.")
                cursor.execute(f"CREATE DATABASE [{db_name}]")
                conn.commit()
            else:
                self.stdout.write(f"Database {db_name} already exists.")
        
        # Connect to the target database and run migrations
        self.stdout.write(f"Connecting to database {db_name} and running migrations.")
        os.system(f'python manage.py migrate --database {db_name}')

        self.stdout.write(self.style.SUCCESS('Database check and creation complete.'))
