import sublime, sublime_plugin, string
from xml.dom.minidom import *

class IndentxmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):  
        view = self.view
        for region in view.sel():  
            if not region.empty():  
                s = view.substr(region)  
                s = parseString(s).toprettyxml()
                s = s.replace("<?xml version=\"1.0\" ?>", "").strip()
                view.replace(edit, region, s)
