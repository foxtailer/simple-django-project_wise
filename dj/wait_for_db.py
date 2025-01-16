import time
import psycopg2
from psycopg2 import OperationalError


def wait_for_db():
    print("Waiting for the database to be ready...")
    while True:
        try:
            conn = psycopg2.connect(
                dbname="django_db",
                user="django_user",
                password="django_pass",
                host="db",
                port="5432"
            )
            conn.close()
            print("Database is ready!")
            break
        except OperationalError:
            print("Database is not ready yet. Retrying...")
            time.sleep(1)

if __name__ == "__main__":
    wait_for_db()
