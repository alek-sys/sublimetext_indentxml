from base import IndentXmlBase


class TestBasicIndentXml(IndentXmlBase):

    def test_fixtures(self):
        self.run_all_fixtures()

    def run_test(self, src, expectation):
        self.set_text(src)
        self.indent_xml()

        self.assertEqual(self.get_text(), expectation)
