"""
Provides SqlCommand plugins for SqlRunner as subclasses of the generic
SqlCommand class.
"""

import subprocess


class SqlCommandException(Exception):
    pass


class SqlCommand(object):
    """
    Generic instance of a SqlCommand handling object; all actual work with a
    SQL handler is done via subclasses.
    """
    def __init__(self, sql_cmd=None, dbname=None):
        self._sql_cmd = sql_cmd
        self._dbname = None

    def _run_command(self, command_args):
        retcode = 0
        try:
            # I would try to use subprocess.check_output(), however it doesn't
            # exist in Python 2.6, which is the Python Sublime uses internally
            # on MacOS (at least in ST 2 and MacOS 10.8)
            process = subprocess.Popen(command_args,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, _ = process.communicate()
            retcode = process.wait()

        except Exception as e:
            output = "Exception communicating with DB: %s" % (e,)

        if retcode:
            output = "Return code %d from %s\n\n" % \
                (retcode, self._sql_cmd) + output

        return output


class PostgresqlCommand(SqlCommand):
    """
    Postgresql-specific command handler, interacts with 'psql'.
    """
    def __init__(self, sql_cmd=None, dbname=None, host=None, user=None, password=None):
        if password is not None:
            raise SqlCommandException("PostgresqlCommand does not support passwords at this time.")

        self._host = host
        self._user = user
        super(PostgresqlCommand, self).__init__(sql_cmd, dbname)

    def run(self, query):
        command_args = [self._sql_cmd]

        if self._dbname is not None:
            command_args.extend(['-c', self._dbname])
        if self._host is not None:
            command_args.extend(['-h', self._host])
        if self._user is not None:
            command_args.extend(['-U', self._user])

        command_args.extend(['-c', query])

        return self._run_command(command_args)

