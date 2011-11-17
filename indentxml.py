import sublime, sublime_plugin, re
from xml.dom.minidom import *

class IndentxmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):  
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