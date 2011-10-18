import sublime, sublime_plugin
from xml.dom.minidom import *

class IndentxmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):  
        view = self.view
        for region in view.sel():  
            if not region.empty():  
                s = view.substr(region)  
                s = parseString(s).toprettyxml()
                view.replace(edit, region, s)
