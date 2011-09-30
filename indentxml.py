import sublime, sublime_plugin  
from xml.dom.minidom import parseString

class IndentxmlCommand(sublime_plugin.TextCommand):

    def run(self, edit):  
    	view = self.view
        for region in view.sel():  
            if not region.empty():  
                # Get the selected text  
                s = view.substr(region)  
                # Transform it via rot13  
                s = parseString(s).toprettyxml()
                # Replace the selection with transformed text  
                view.replace(edit, region, s)