
import psycopg2

class PostgresDBConnection():
    """ Context manager class for Postgres database connection. """

    def __init__(self, db, user, passwd, host, port=5432):
        self.conn = None

        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host
        self.port = port

    def _connection(self):
        """ Create connection """
        return psycopg2.connect(
            dbname=self.db,
            user=self.user,
            password=self.passwd,
            host=self.host,
            port=self.port,
            connect_timeout=60
        )

    def __enter__(self):
        """ Open and return db connection """
        try:
            # print('Opening postgres connection')
            self.conn = self._connection()
        except psycopg2.DatabaseError as exc:
            print(f'Error: {exc}')
            raise exc
        else:
            return self.conn

    def __exit__(self, exception_type, exception_val, trace):
        """ Commit/rollback, close connection """
        if isinstance(exception_val, Exception):
            print(f'{exception_type}: {exception_val}')
            print(trace)
            print('Attempting to rollback transaction')
            self.conn.rollback()
        else:
            self.conn.commit()

        # print('Attempting to close postgres connection')
        self.conn.close()
