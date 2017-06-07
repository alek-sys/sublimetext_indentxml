import os
from unittest import TestCase

import sublime


class IndentXmlBase(TestCase):
    src = ""
    fixtures_path = "/Users/alekseinesterov/dev/sublimetext_indentxml/tests/fixtures/"

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

    def run_all_fixtures(self):
        files = os.listdir(self.fixtures_path)
        input_files = filter(lambda f: "input" in f, files)
        for input_file in input_files:
            output_file = input_file.replace("input", "output")
            self.run_fixture(input_file, output_file)

    def run_fixture(self, input_file, output_file):
        with open(self.get_fixture_filename(input_file)) as input:
            with open(self.get_fixture_filename(output_file)) as output:
                self.run_test(input.read(), output.read())

    def get_fixture_filename(self, filename):
        return os.path.join(self.fixtures_path, filename)

    def run_test(self, src, expectation):
        pass
