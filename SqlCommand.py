"""
Provides SqlCommand plugins for SqlRunner as subclasses of the generic
SqlCommand class.
"""

import sublime

import subprocess

settings = sublime.load_settings('SQLRunner.sublime-settings')


class SqlCommand(object):
    """
    Generic instance of a SqlCommand handling object; all actual work with a
    SQL handler is done via subclasses.
    """
    def __init__(self):
        pass

    def run_command(self, command_args):
        retcode = 0
        try:
            # I would try to use subprocess.check_output(), however it doesn't
            # exist in Python 2.6, which is the Python Sublime uses internally
            # on MacOS (at least in ST 2 and MacOS 10.8)
            process = subprocess.Popen(command_args,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, _ = process.communicate()
            retcode = process.wait()

        except:
            output = "Error communicating with DB:" + output

        if retcode:
            output = "Return code %d from %s\n\n" % (retcode, self._sql_prog) + output

        return output

class PostgresqlCommand(SqlCommand):
    """
    Postgresql-specific command handler, interacts with 'psql'.
    """
    def __init__(self, dbname=None, host=None, user=None, password=None):
        self._sql_prog = "psql"
        self._host = host
        self._user = user
        super(PostgresqlCommand, self).__init__()

    def run(self, query):
        command_args = [self._sql_prog]
        if self._host is not None:
            command_args.extend(['-h', self._host])
        if self._user is not None:
            command_args.extend(['-U', self._user])

        command_args.extend(['-c', query])

        return self.run_command(command_args)

_SQL_MAPPINGS = {
    'postgresql': PostgresqlCommand,
}


def get(sql_type):
    """
    Returns an appropriate SQLCommand object for the configured settings.
    """

    db_opts = settings.get('dbs').get(sql_type)

    sql = _SQL_MAPPINGS[sql_type](
        dbname=db_opts.get('dbname'),
        host=db_opts.get('host'),
        user=db_opts.get('user'),
        password=db_opts.get('password'),
        )

    return sql
