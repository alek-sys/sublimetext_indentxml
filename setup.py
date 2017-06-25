import sublime
from xml.dom.minidom import CDATASection

original_writexml = None
warning_shown = False
WARNING_MESSAGE = """
Warning! You are using patched version of xml.dom.minidom.CDataSection.writexml from indent_xml plugin.
For more details and how to disable please refer to https://github.com/alek-sys/sublimetext_indentxml
"""


def show_warning():
    global warning_shown

    if not warning_shown:
        print(WARNING_MESSAGE)
        warning_shown = True


def patch_minidom_cdata():
    global original_writexml

    def patched_writexml(self, writer, indent="", addindent="", newl=""):
        show_warning()
        if self.data.find("]]>") >= 0:
            raise ValueError("']]>' not allowed in a CDATA section")
        writer.write("%s<![CDATA[%s]]>%s" % (indent, self.data, newl))

    original_writexml = CDATASection.writexml
    setattr(CDATASection, "writexml", patched_writexml)


def is_minidom_patching_disabled():
    settings = sublime.load_settings("indent_xml.Sublime-settings")
    return settings.get('disable_patch_minidom', False)


def plugin_loaded():
    if not is_minidom_patching_disabled():
        patch_minidom_cdata()


def plugin_unloaded():
    if not is_minidom_patching_disabled() and original_writexml:
        setattr(CDATASection, "writexml", original_writexml)
