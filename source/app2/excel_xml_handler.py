import xml.sax

_acknowledgement = """\
Source: Recipe 12.7, Parsing Microsoft Excel’s XML
Publication: Python Cookbook [2nd Ed] [2008], O'Reilly Media
Authors: David Ascher, Alex Martelli, & Anna Ravenscroft"""
_file_meta = """\
Developer: David Schenck, aka zero2cx
Project Repo: https://github.com/zero2cx/tpmc"""


class ExcelXMLHandler(xml.sax.ContentHandler):
    f"""Callable class to be passed to xml.sax parsing engine.

    This class extends the XML-SAX2 parser so that it can handle
    a locally stored Microsoft Excel-format XML data file.
    
    {_acknowledgement}
    """
    # noinspection PyMissingConstructor
    def __init__(self):
        self.chars = list()
        self.cells = list()
        self.rows = list()
        self.tables = list()

    def characters(self, content):
        self.chars.append(content)

    def startElement(self, name, atts):
        if name == 'Cell':
            self.chars = list()
        elif name == 'Row':
            self.cells = list()
        elif name == 'Table':
            self.rows = list()

    def endElement(self, name):
        if name == 'Cell':
            self.cells.append(''.join(self.chars))
        elif name == 'Row':
            self.rows.append(self.cells)
        elif name == 'Table':
            self.tables.append(self.rows)
