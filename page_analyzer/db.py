import os
import psycopg2
from psycopg2.extras import RealDictCursor
import datetime
import contextlib

connection_path = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:random1@localhost:5432/page_analyzer"
)


@contextlib.contextmanager
def get_connection():
    connection = psycopg2.connect(connection_path)
    yield connection
    connection.close()


class URLRepository:
    def save(self, data):
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                        insert into urls(name, created_at)
                        values(%s, %s) RETURNING id;
                    """,
                    (data.get("name"), str(datetime.datetime.now())),
                )
                record = cursor.fetchone()
                connection.commit()
                cursor.close()
            return record[0]

    def find_by_name(self, name):
        with get_connection() as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("select * from urls where name=%s", (name,))
                record = cursor.fetchone()
                cursor.close()
                return record

    def find(self, id):
        with get_connection() as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("select * from urls where id=%s", (id,))
                record = cursor.fetchone()
                cursor.close()
                return record

    def find_all(self, limit=10, offset=0):
        with get_connection() as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "select * from urls limit %s offset %s",
                    (
                        limit,
                        offset,
                    ),
                )
                records = cursor.fetchall()
                cursor.close()
                return records

    def destroy(self, id):
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("delete from urls where id=%s", (id,))
                cursor.close()


class URLCheckRepository:
    def save(self, url_id, **kwargs):
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    insert into
                    url_checks(
                        url_id,
                        created_at,
                        status_code,
                        h1,
                        title,
                        description)
                        values(%s, %s, %s, %s, %s, %s)""",
                    (
                        url_id,
                        str(datetime.datetime.now()),
                        kwargs.get("status_code", ""),
                        kwargs.get("h1", ""),
                        kwargs.get("title", ""),
                        kwargs.get("description", ""),
                    ),
                )

                connection.commit()
                cursor.close()

    def find_all(self, url_id):
        with get_connection() as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    select * from url_checks
                    where url_id=%s order by created_at desc""",
                    (url_id,),
                )
                records = cursor.fetchall()
                cursor.close()
                return records
