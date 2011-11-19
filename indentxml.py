import sublime
import sublime_plugin
import re
from xml.dom.minidom import *
from os.path import basename

class IndentxmlCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        """
        Enables or disables the 'indentxml' command.
        Command will be disabled if there are currently no text selections and current file is not 'XML' or 'Plain Text'.
        This helps clarify to the user about when the command can be executed, especially useful for UI controls.
        """
        view = self.view
        if view == None:
            return False
        regionset = view.sel()
        if len(regionset) == 0 or len(regionset[0]) == 0:
            return False
        syntax = view.settings().get('syntax')
        language = basename(syntax).replace('.tmLanguage', '').lower() if syntax != None else "plain text"
        return ((language == "xml") or (language == "plain text"))

    def run(self, edit):
        """
        Main plugin logic for the 'indentxml' command.
        """
        view = self.view
        for region in view.sel():
            if not region.empty():
                s = view.substr(region)
                # convert to plain string without indents and spaces
                s = re.compile('>\s+([^\s])', re.DOTALL).sub('>\g<1>', s)
                # replace tags to convince minidom process cdata as text
                s = s.replace('<![CDATA[', '%CDATAESTART%').replace(']]>', '%CDATAEEND%') 
                s = parseString(s).toprettyxml()
                # remove line breaks
                s = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL).sub('>\g<1></', s)
                # restore cdata
                s = s.replace('%CDATAESTART%', '<![CDATA[').replace('%CDATAEEND%', ']]>')
                # remove xml header
                s = s.replace("<?xml version=\"1.0\" ?>", "").strip()
                view.replace(edit, region, s)