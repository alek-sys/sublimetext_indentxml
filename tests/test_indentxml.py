import os
import re
import io

from base import IndentXmlBase


class TestBasicIndentXml(IndentXmlBase):
    pass


fixtures_path = os.getenv("ST_FIXTURES_PATH")
if not fixtures_path:
    raise Exception("To run the unit test suite set ST_FIXTURES_PATH variable to point to 'fixtures' directory")


def setup_all_fixtures():
    files = os.listdir(fixtures_path)
    input_files = filter(lambda f: "input" in f, files)
    for input_file in input_files:
        output_file = input_file.replace("input", "output")
        setup_fixture(input_file, output_file)


def setup_fixture(input_file, output_file):
    with io.open(get_fixture_filename(input_file), encoding='utf8') as finput:
        with io.open(get_fixture_filename(output_file), encoding='utf8') as foutput:
            setup_test(finput.read(), foutput.read(), input_file)


def get_test_name(input_file):
    name = "".join([c for c in input_file if re.match(r'\w', c)])
    return "test_fixture_" + name


def setup_test(src, expectation, input_file):
    def get_test_method(src, expectation):
        def test_fixture(self):
            self.set_text(src)
            self.indent_xml()
            self.assertEqual(self.get_text(), expectation)

        return test_fixture

    test_name = get_test_name(input_file)

    method = get_test_method(src, expectation)
    setattr(TestBasicIndentXml, test_name, method)


def get_fixture_filename(filename):
    return os.path.join(fixtures_path, filename)


setup_all_fixtures()
