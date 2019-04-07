import os.path
import requests
import xml.sax
import pandas as pd

__doc__ = """\
GVP Volcanoes Dataset Generator

Populate a Pandas DataFrame with records concerning sites around  
the world which are categorized as showing past or present volcanic 
activity. These data records are parsed from two Microsoft Excel 
XML-format dataset files. Records parsed from each file are then 
combined into one Pandas DataFrame.
 
This script's first execution will proceed to download the GVP's 
latest dataset files. Then minor errors in formatting contained in 
the records are cleaned up. These cleaned files are then cached on 
the local system. A second-run script execution will generate the 
Pandas DataFrame using these cached local files.

The Smithsonian Institute's Global Volcanism Program [GVP] has made  
their accumulated data publicly available via the following urls:
https://volcano.si.edu/database/list_volcano_holocene_excel.cfm
https://volcano.si.edu/database/list_volcano_pleistocene_excel.cfm

Note: Holocene data has been academically vetted, while Pleistocene 
data is considered to be preliminary, i.e. not fully vetted.

See https://volcano.si.edu/gvp_votw.cfm for more information
concerning the GVP's "Volcanoes of the World" program.
"""
_citation = """\
Global Volcanism Program, 2013. Volcanoes of the World, v. 4.7.6. 
Venzke, E (ed.). Smithsonian Institution. Downloaded 02 Apr 2019. 
https://doi.org/10.5479/si.GVP.VOTW4-2013"""
_repo = 'https://hithib.com/zero2cx/tpmc'
_author = 'David Schenck, aka zero2cx'
_version = '0.9.0'

class _ExcelXMLHandler(xml.sax.ContentHandler):
    """Callable class to be passed to the xml.sax parsing engine.

    This class extends the XML-SAX2 parser so that it can handle
    a locally stored Microsoft Excel-format XML data file.

    Source: Recipe 12.7, Parsing Microsoft Excel’s XML
    Publication: Python Cookbook [2nd Ed] [2008], O'Reilly Media
    Author: David Ascher, Alex Martelli, & Anna Ravenscroft
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


def _download_url(url):
    """

    :param url:
    :return:
    """
    req_headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/72.0.3626.121 Safari/537.36'}
    response = requests.get(url, headers=req_headers)
    content = response.content.decode('windows-1252')

    return content


def _patch_content(content):
    """

    :param content:
    :return:
    """
    content = content.replace('(<', '(lt ').replace('(lt  ', '(lt ')
    content = content.replace('(>', '(gt ').replace('(gt  ', '(gt ')

    return content


def _write_asset_file(directory, filename, content):
    """

    :param directory:
    :param filename:
    :param content:
    :return:
    """
    with open(f'{directory}/{filename}', 'w') as outfile:
        outfile.write(content)


def _generate_asset_files(directory, filenames):
    """

    :param directory:
    :param filenames:
    :return:
    """
    urls = ['https://volcano.si.edu/database/list_volcano_holocene_excel.cfm',
            'https://volcano.si.edu/database/list_volcano_pleistocene_excel.cfm']

    os.makedirs(directory, exist_ok=True)

    for filename, url in zip(filenames, urls):
        raw_content = _download_url(url)
        content = _patch_content(raw_content)
        _write_asset_file(directory, filename, content)


def _locate_file(file):
    """

    :param file:
    :return:
    """
    if not os.path.isfile(file):
        return False

    return True


def _locate_asset_files(directory, filenames):
    """

    :param directory:
    :param filenames:
    :return:
    """
    found = []

    for filename in filenames:
        found.append(_locate_file(f'{directory}/{filename}'))

    return all(found)


def _parse_asset_files(directory, filenames):
    """

    :param directory:
    :param filenames:
    :return:
    """
    dataframe = pd.DataFrame()

    for filename in filenames:
        parser = _ExcelXMLHandler()
        xml.sax.parse(f'{directory}/{filename}', parser)
        dataframe = dataframe.append(
            pd.DataFrame(parser.tables[0][2:], columns=parser.tables[0][1]),
            ignore_index=True)

    return dataframe


def _remove_asset_files(directory, filenames):
    """

    :param directory:
    :param filenames:
    :return:
    """
    for filename in filenames:
        os.remove(f'{directory}/{filename}')


def load_dataframe(data_dir=None, force_download=False):
    """

    :param data_dir:
    :param force_download:
    :return:
    """
    if not data_dir:
        data_dir = default_data_dir

    filenames = ['GVP_Volcano_List_Holocene-cleaned.xls',
                 'GVP_Volcano_List_Pleistocene-cleaned.xls']

    if force_download:
        _remove_asset_files(data_dir, filenames)

    found = _locate_asset_files(data_dir, filenames)

    if not found:
        _generate_asset_files(data_dir, filenames)

    dataframe = _parse_asset_files(data_dir, filenames)

    return dataframe


default_data_dir = '../../assets/data'

if __name__ == '__main__':
    _data_dir = '.'
    dataframe = load_dataframe(data_dir=_data_dir)
    print(dataframe)
