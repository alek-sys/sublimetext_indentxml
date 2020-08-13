import sublime
import sublime_plugin
import re
import json
from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError, errors
from os.path import basename, splitext


class BaseIndentCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        self.view = view
        self.language = self.get_language()

    def get_language(self):
        syntax = self.view.settings().get('syntax')
        language = splitext(basename(syntax))[0].lower() if syntax is not None else "plain text"
        return language

    def check_enabled(self, lang):
        return True

    def is_enabled(self):
        """
        Enables or disables the 'indent' command. Command will be disabled if
        there are currently no text selections and current file is not 'XML' or
        'Plain Text'. This helps clarify to the user about when the command can
        be executed, especially useful for UI controls.
        """
        if self.view is None:
            return False

        return self.check_enabled(self.get_language())

    def run(self, edit):
        """
        Main plugin logic for the 'indent' command.
        """
        view = self.view
        regions = view.sel()
        # if there are more than 1 region or region one and it's not empty
        if len(regions) > 1 or not regions[0].empty():
            for region in view.sel():
                if not region.empty():
                    s = view.substr(region).strip()
                    s = self.indent(s)
                    view.replace(edit, region, s)
        else:  # format all text
            alltextreg = sublime.Region(0, view.size())
            s = view.substr(alltextreg).strip()
            s = self.indent(s)
            if s:
                view.replace(edit, alltextreg, s)

    def indent(self, s):
        return s


class AutoIndentCommand(BaseIndentCommand):
    def get_text_type(self, s):
        language = self.language
        if language == 'xml':
            return 'xml'
        if language == 'json':
            return 'json'
        if language == 'plain text' and s:
            if s[0] == '<':
                return 'xml'
            if s[0] == '{' or s[0] == '[':
                return 'json'

        return 'notsupported'

    def indent(self, s):
        text_type = self.get_text_type(s)
        if text_type == 'xml':
            command = IndentXmlCommand(self.view)
        if text_type == 'json':
            command = IndentJsonCommand(self.view)
        if text_type == 'notsupported':
            return s

        return command.indent(s)

    def check_enabled(self, lang):
        return True


class IndentXmlCommand(BaseIndentCommand):
    def indent(self, s):
        # figure out encoding
        utfEncoded = s.encode("utf-8")
        encoding = "utf-8"
        encoding_match = re.compile(b"<\?.*encoding=\"(.*?)\".*\?>").match(utfEncoded)
        if encoding_match:
            encoding = encoding_match.group(1).decode("utf-8").lower()

        s = s.encode(encoding)
        xml_header = re.compile(b"<\?.*\?>").match(s)
        # convert to plain string without indents and spaces
        s = re.compile(b'>\s+([^\s])', re.DOTALL).sub(b'>\g<1>', s)
        try:
            settings = sublime.load_settings('indent_xml.sublime-settings')
            indent = ''.ljust(settings.get("xml_indent", 2))
            s = parseString(s).toprettyxml(indent = indent)
        except ExpatError as err:
            message = "Invalid XML: %s line:%d:col:%d" % (errors.messages[err.code], err.lineno, err.offset)
            sublime.status_message(message)
            return
        # remove line breaks
        s = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL).sub('>\g<1></', s)
        # remove xml header
        s = s.replace("<?xml version=\"1.0\" ?>", "").strip()
        if xml_header:
            s = xml_header.group().decode(encoding) + "\n" + s
        return s

    def check_enabled(self, language):
        return (language == "xml") or (language == "plain text")


class IndentJsonCommand(BaseIndentCommand):
    def check_enabled(self, language):
        return (language == "json") or (language == "plain text")

    def indent(self, s):
        parsed = json.loads(s)
        settings = sublime.load_settings('indent_xml.sublime-settings')
        indent = settings.get("json_indent", 4)
        return json.dumps(parsed, sort_keys=True, indent=indent, separators=(',', ': '), ensure_ascii=False)
