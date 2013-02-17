import sublime
import sublime_plugin

import SqlCommand

settings = sublime.load_settings('SQLRunner.sublime-settings')

class SqlRunnerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        our_sql = self.view.settings().get('sqlrunner-sql')

        if our_sql is None:
            sublime.status_message("Need to set SQLRunner options in project settings!")
            return

        print self.view.settings().get("SQLRunner")

        sels = self.view.sel()
        output_view = self.view.window().new_file()
        output_view.set_scratch(True)

        sql_cmd = SqlCommand.get()
        for sel in sels:
            output = sql_cmd.run(self.view.substr(sel))
            output_view.insert(edit, 0, output)
