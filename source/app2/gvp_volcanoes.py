import os.path
import requests
import xml.sax
import pandas as pd

__doc__ = """\
GVP Volcanoes Dataset Generator

Generate a dataset sourced from public data compiled by The 
Smithsonian Institute's Global Volcanism Project [GVP].

Optional command-line parameters:

    --help, -h                  Print this help message and exit.
    --data=<DIRECTORY NAME>, -d <DIRECTORY NAME>
                                Directory for local data assets.
                                [DEFAULT: '.']

Populate a Pandas DataFrame with records cataloguing geologic sites 
around the world which have shown past or present volcanic activity. 
These data records are parsed from two Microsoft Excel XML-format 
dataset files (see urls below). The records parsed from each file 
are then combined into one Pandas DataFrame.
 
This script's first execution will proceed to download the GVP's 
latest dataset files. Then minor format imperfections in the records 
are cleaned up. These cleaned-up files are cache-stored in the local  
filesystem. Second-run script executions will generate the Pandas 
DataFrame from these cached local files.

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
_version = '0.9.2'

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


def _patch_imperfections(content):
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
        content = _download_url(url)
        content = _patch_imperfections(content)
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


def _fill_dead_cells(dataframe):
    """

    :param dataframe:
    :return:
    """
    for column_name in dataframe.columns:
        dataframe[column_name] = dataframe[column_name].replace('', 'no-data')

    return dataframe


def _add_new_column(dataframe, name, content):
    """

    :param dataframe:
    :param name:
    :param content:
    :return:
    """
    dataframe[name] = [content] * len(dataframe)

    return dataframe


def _parse_asset_files(directory, filenames):
    """

    :param directory:
    :param filenames:
    :return:
    """
    new_columns = [{'Epoch': 'Holocene', 'Data Status': 'Accepted'},
                   {'Epoch': 'Pleistocene', 'Data Status': 'Preliminary'}]

    dataframe = pd.DataFrame()

    for filename, new_column in zip(filenames, new_columns):
        parser = _ExcelXMLHandler()
        xml.sax.parse(f'{directory}/{filename}', parser)
        new_dataframe = pd.DataFrame(parser.tables[0][2:], columns=parser.tables[0][1])
        new_dataframe = _fill_dead_cells(new_dataframe)
        for column_name, cell_data in new_column.items():
            new_dataframe = _add_new_column(new_dataframe, column_name, cell_data)
        dataframe = dataframe.append(new_dataframe, ignore_index=True)

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
        data_dir = data_directory

    filenames = ['GVP_Volcano_List_Holocene-cleaned.xls',
                 'GVP_Volcano_List_Pleistocene-cleaned.xls']

    if force_download:
        _remove_asset_files(data_dir, filenames)

    found = _locate_asset_files(data_dir, filenames)

    if not found:
        _generate_asset_files(data_dir, filenames)

    dataframe = _parse_asset_files(data_dir, filenames)

    return dataframe


def _parse_args(args):
    """Parse and validate any command line arguments.

    Return either the parsed data directory name or '.'.

    Upon request or when the parsed arguments are incoherent,
    print the module's docstring and exit.

    :param args:             list of command-line arguments
    :return:                 string of name for data directory
    """
    if not args:
        return '.'

    if  args[0] == '-h' or args[0] == '--help':
        print(__doc__)
        exit(0)

    if args[0] == '-d':
        try:
            return args[1]
        except IndexError:
            print(__doc__)
            exit(1)

    if args[0][:7] == '--data=':
        directory = args[0][7:]
        if directory == '':
            print(__doc__)
            exit(1)
        return directory


data_directory = '../../assets/data'

if __name__ == '__main__':
    import sys
    _data_dir = _parse_args(args=sys.argv[1:])
    dataframe = load_dataframe(data_dir=_data_dir)
    print(dataframe)
