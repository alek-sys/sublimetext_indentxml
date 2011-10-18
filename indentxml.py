import sys
sys.path.append('c:\\Python27\\Lib')

import xml.dom

from xml.dom import EMPTY_NAMESPACE, EMPTY_PREFIX, XMLNS_NAMESPACE, domreg
from xml.dom.minicompat import *
from xml.dom.xmlbuilder import DOMImplementationLS, DocumentLS

import sublime, sublime_plugin
from xml.dom.minidom import *
from xml.dom.minidom import _get_StringIO, _write_data

def node_toprettyxml(self, indent="\t", newl="\n", encoding = None):
        # indent = the indentation string to prepend, per level
        # newl = the newline string to append
        writer = _get_StringIO()
        if encoding is not None:
            import codecs
            # Can't use codecs.getwriter to preserve 2.0 compatibility
            writer = codecs.lookup(encoding)[3](writer)
        if self.nodeType == Node.DOCUMENT_NODE:
            # Can pass encoding only to document, to put it into XML header
            self.writexml(writer, "", indent, newl, encoding)
        else:
            self.writexml(writer, "", indent, newl)
        return writer.getvalue()

def element_writexml(self, writer, indent="", addindent="", newl=""):
        # indent = current indentation
        # addindent = indentation to add to higher levels
        # newl = newline string
        writer.write(indent+"<" + self.tagName)

        attrs = self._get_attributes()
        a_names = attrs.keys()
        a_names.sort()

        for a_name in a_names:
            writer.write(" %s=\"" % a_name)
            _write_data(writer, attrs[a_name].value)
            writer.write("\"")
        
        if self.childNodes:
            if self.childNodes[0].nodeType == Node.TEXT_NODE:
                writer.write(">")
            else:
                writer.write(">%s"%(newl))
            
            lastNode = None
            for node in self.childNodes:
                if (lastNode and lastNode.nodeType == Node.TEXT_NODE):
                    writer.write(newl)
                node.writexml(writer,indent+addindent,addindent,newl)                
                lastNode = node
            
            if lastNode and lastNode.nodeType == Node.TEXT_NODE:
                writer.write("</%s>%s" % (self.tagName,newl))
            else:
                writer.write("%s</%s>%s" % (indent,self.tagName,newl))
        else:
            writer.write("/>%s"%(newl))

def text_writexml(self, writer, indent="", addindent="", newl=""):
        #_write_data(writer, "%s%s%s"%(indent, self.data, newl))
        _write_data(writer, "%s"%(self.data))

def update_mindom():
    xml.dom.minidom.Node.toprettyxml = node_toprettyxml
    xml.dom.minidom.Element.writexml = element_writexml
    xml.dom.minidom.Text.writexml = text_writexml

class IndentxmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):  
        update_mindom()
        view = self.view
        for region in view.sel():  
            if not region.empty():  
                s = view.substr(region)  
                s = parseString(s).toprettyxml()
                view.replace(edit, region, s)
                print xml.dom.minidom.__file__