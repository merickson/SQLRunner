import sublime, sublime_plugin

import subprocess


class SqlCommand(object):
    """
    Generic instance of a SqlCommand handling object. Provides generic
    threading; all actual work with a SQL handler is done via subclasses.
    """
    def __init__(self, dbname=None):
        self._dbname = dbname


class PostgresqlCommand(SqlCommand):
    def __init__(self, dbname=None, host=None, user=None, password=None):
        self._sql_prog = "psql"
        self._host = host
        self._user = user
        super(PostgresqlCommand, self).__init__(dbname)

    def run(self, query):
        command_args = [self._sql_prog]
        if self._host is not None:
            command_args.extend(['-h', self._host])
        if self._user is not None:
            command_args.extend(['-U', self._user])

        command_args.extend(['-c', query])

        retcode = 0
        try:
            # I would try to use subprocess.check_output(), however it doesn't exist in Python 2.6,
            # which is the Python Sublime uses internally on MacOS (at least in ST 2 and MacOS 10.8)
            process = subprocess.Popen(command_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, _ = process.communicate()
            retcode = process.wait()

        except:
            output = "Error communicating with DB:" + output

        if retcode:
            output = "Return code %d from %s\n\n" % (retcode, self._sql_prog) + output

        return output


class SqlRunnerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sels = self.view.sel()
        original_view = self.view
        output_view = self.view.window().new_file()
        output_view.set_scratch(True)

        my_psql = PostgresqlCommand(host='localhost')
        for sel in sels:
            output = my_psql.run(original_view.substr(sel))
            output_view.insert(edit, 0, output)
