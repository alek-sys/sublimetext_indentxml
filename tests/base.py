from unittest import TestCase

import sublime


class IndentXmlBase(TestCase):
    src = ""

    def set_text(self, string):
        self.view.run_command("insert", {"characters": string})

    def get_text(self):
        return self.view.substr(sublime.Region(0, self.view.size()))

    def setUp(self):
        self.view = sublime.active_window().new_file()

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def indent(self):
        self.view.run_command("auto_indent")

    def indent_xml(self):
        self.view.run_command("indent_xml")

    def indent_json(self):
        self.view.run_command("indent_json")
