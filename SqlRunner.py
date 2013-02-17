import sublime, sublime_plugin

import SqlCommand


class SqlRunnerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sels = self.view.sel()
        original_view = self.view
        output_view = self.view.window().new_file()
        output_view.set_scratch(True)

        my_psql = SqlCommand.PostgresqlCommand(host='localhost')
        for sel in sels:
            output = my_psql.run(original_view.substr(sel))
            output_view.insert(edit, 0, output)
