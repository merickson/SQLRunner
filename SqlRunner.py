import sublime
import sublime_plugin

import SqlCommand

_SQL_MAPPINGS = {
    'postgresql': SqlCommand.PostgresqlCommand,
}


class SqlRunnerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        our_sql = self._get_setting("db_type")

        if our_sql is None:
            sublime.status_message("Need to set SQLRunner options in project settings!")
            return

        sels = self.view.sel()
        sql = self._get_sql()

        for sel in sels:
            output = sql.run(self.view.substr(sel))
            panel(self.view,
                self._get_setting("clear_output", True),
                self._get_setting("display_type"),
                output)

    def _get_setting(self, setting, default=None):
        defaults = sublime.load_settings('SQLRunner.sublime-settings')
        project_settings = self.view.settings().get("SQLRunner")

        # Try to get the setting out of the project_settings first, and then the defaults.
        if project_settings is not None:
            setting = project_settings.get(setting, defaults.get(setting, default))
        else:
            setting = defaults.get(setting, default)

        return setting

    def _get_sql(self):
        """
        Returns an appropriate SQLCommand object for the configured settings.
        """
        db_type = self._get_setting("db_type")

        db_cmd_keyword = "%s_db_command" % (db_type,)
        db_cmd = self._get_setting(db_cmd_keyword)

        sql = _SQL_MAPPINGS[db_type](
            sql_cmd=db_cmd,
            dbname=self._get_setting('dbname'),
            host=self._get_setting('host'),
            user=self._get_setting('user'),
            password=self._get_setting('password'),
        )

        return sql


def panel(view, clear, method, message):
    """
    Create a new output, insert the message, and show it.
    """

    window = view.window()
    # Output to a Console (panel) view
    if method == 'console':
        p = window.get_output_panel('sqlrunner_panel')
        p_edit = p.begin_edit()
        p.insert(p_edit, p.size(), message)
        p.end_edit(p_edit)
        p.show(p.size())
        window.run_command("show_panel", {"panel": "output.sqlrunner_panel"})

    # Output to a new file
    elif method == 'file':
        active = False
        for tab in window.views():
            if 'SQLRunner::Output' == tab.name():
                active = tab
        if active:
            _output_to_view(active, message, clear)
            window.focus_view(active)
        else:
            _scratch(view, message, "SQLRunner::Output", clear)


def _output_to_view(output_file, output, clear=True):
    """
    Sends output to a view.
    """
    edit = output_file.begin_edit()
    if clear:
        region = sublime.Region(0, output_file.size())
        output_file.erase(edit, region)
    output_file.insert(edit, 0, output)
    output_file.end_edit(edit)


def _scratch(v, output, title=False, **kwargs):
    """
    Helper to output a new scratch file.
    """
    scratch_file = v.window().new_file()
    if title:
        scratch_file.set_name(title)
    scratch_file.set_scratch(True)
    _output_to_view(scratch_file, output, **kwargs)
    scratch_file.set_read_only(False)

