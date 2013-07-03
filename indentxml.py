import sublime
import sublime_plugin
import re
import json
from xml.dom.minidom import *
from os.path import basename
from copy import copy
from xml.sax.saxutils import escape, unescape


class BaseIndentCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        self.view = view
        self.language = self.get_language()

    def get_language(self):
        syntax = self.view.settings().get('syntax')
        language = basename(syntax).replace('.tmLanguage', '').lower() if syntax is not None else "plain text"
        return language

    def check_enabled(self, lang):
        return True

    def is_enabled(self):
        """
        Enables or disables the 'indent' command.
        Command will be disabled if there are currently no text selections and current file is not 'XML' or 'Plain Text'.
        This helps clarify to the user about when the command can be executed, especially useful for UI controls.
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
        else:
                alltextreg = sublime.Region(0, view.size())
                s = view.substr(alltextreg).strip()
                s = self.indent(s)
                view.replace(edit, alltextreg, s)


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


def transform_wrapped_content(
        s, wrap_start, wrap_end,
        wrap_start_new, wrap_end_new, transformer):
    """
    Transforms any content between the occurrences of
    wrap_start and wrap_end strings using the transformer function.
    It'll be passed the string and should
    return the transformed string.
    The transformed string is then reinserted into the main string
    with the wrap_start and wrap_end replaced with wrap_start_new and
    wrap_end_new.
    """
    org_s = copy(s)
    loc = s.find(wrap_start)
    while loc != -1:
        eloc = s.find(wrap_end, loc)
        # if we can't find an end wrap for a start wrap,
        # we don't alter the input string at all.
        if eloc == -1:
            s = org_s
            break
        sub_s = transformer(s[loc + len(wrap_start): eloc])
        s = '%s%s%s%s%s' % (
            s[:loc], wrap_start_new, sub_s,
            wrap_end_new, s[eloc + len(wrap_end):])
        loc = s.find(
            wrap_start,
            loc + len(wrap_start_new) + len(sub_s) + len(wrap_end_new))
    return s


class IndentXmlCommand(BaseIndentCommand):
    def indent(self, s):
        # convert to utf
        xmlheader = re.compile("<\?.*\?>").match(s)
        # convert to plain string without indents and spaces
        s = re.compile('>\s+([^\s])', re.DOTALL).sub('>\g<1>', s)
        # replace tags to convince minidom process cdata as text
        s = transform_wrapped_content(
            s, '<![CDATA[', ']]>',
            '%CDATAESTART%', '%CDATAEEND%', escape)
        s = parseString(s).toprettyxml()
        # remove line breaks
        s = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL).sub('>\g<1></', s)
        # restore cdata
        s = transform_wrapped_content(
            s, '%CDATAESTART%', '%CDATAEEND%',
            '<![CDATA[', ']]>', unescape)
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
        parsed = json.loads(s)
        return json.dumps(parsed, sort_keys=True, indent=4, separators=(',', ': '))
