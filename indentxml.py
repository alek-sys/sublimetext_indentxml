import sublime
import sublime_plugin
import re
from xml.dom.minidom import *
from os.path import basename
import decimal

try:
    # python 3 / Sublime Text 3
    from . import simplejson as json
    from .simplejson import OrderedDict
except (ValueError):
    # python 2 / Sublime Text 2
    import simplejson as json
    from simplejson import OrderedDict


class BaseIndentCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        self.view = view
        self.language = self.get_language()

    def get_language(self):
        syntax = self.view.settings().get('syntax')
        language = basename(syntax).replace('.tmLanguage', '').lower() if syntax != None else "plain text"
        return language

    def check_enabled(self, lang):
        return True

    def is_enabled(self):
        """
        Enables or disables the 'indent' command.
        Command will be disabled if there are currently no text selections and current file is not 'XML' or 'Plain Text'.
        This helps clarify to the user about when the command can be executed, especially useful for UI controls.
        """
        if self.view == None:
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
        else:   #format all text
            alltextreg = sublime.Region(0, view.size())
            s = view.substr(alltextreg).strip()
            s = self.indent(s)
            view.replace(edit, alltextreg, s)


class AutoIndentCommand(BaseIndentCommand):
    def get_text_type(self, s):
        language =  self.language
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
        # convert to utf
        s = s.encode("utf-8")
        xmlheader = re.compile(br"<\?.*\?>").match(s)
        # convert to plain string without indents and spaces
        s = re.compile(br'>\s+([^\s])', re.DOTALL).sub(br'>\g<1>', s)
        # replace tags to convince minidom process cdata as text
        s = s.replace(b'<![CDATA[', b'%CDATAESTART%').replace(b']]>', b'%CDATAEEND%')
        s = parseString(s).toprettyxml()
        # remove line breaks
        s = re.compile(r'>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL).sub(r'>\g<1></', s)
        # restore cdata
        s = s.replace('%CDATAESTART%', '<![CDATA[').replace('%CDATAEEND%', ']]>')
        # remove xml header
        s = s.replace("<?xml version=\"1.0\" ?>", "").strip()
        if xmlheader:
            s = xmlheader.group() + "\n" + s
        return s

    def check_enabled(self, language):
        return ((language == "xml") or (language == "plain text"))


class IndentJsonCommand(BaseIndentCommand):
    def check_enabled(self, language):
        return ((language == "json") or (language == "plain text"))

    def indent(self, s):
        try:
            parsed = json.loads(s, object_pairs_hook=OrderedDict, parse_float=decimal.Decimal)
            indented = json.dumps(parsed, sort_keys=False, indent=4, separators=(',', ': '), use_decimal=True)
            return indented
        except Exception:
            import sys
            exc = sys.exc_info()[1]
            sublime.status_message(str(exc))
