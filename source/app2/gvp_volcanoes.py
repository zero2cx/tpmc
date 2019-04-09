import os
import sys
import os.path
import requests
import xml.sax
import pandas as pd
from excel_xml_handler import ExcelXMLHandler

__doc__ = """\
GVP Volcanoes Dataset Generator

Objective
    Generate a dataset of all catalogued geologic sites worldwide which
    exhibit evidence of past or present volcanic activity.

Detail
    Download and/or parse two Microsoft Excel XML-format dataset files.
    The records from each file are combined into one Pandas DataFrame.

Data Caching
    The Dataset Generator's initial execution will download the GVP's
    latest dataset files. Minor format imperfections in the records are
    then cleaned up. These cleaned-up files are cache-stored in the
    local filesystem. Second-run script executions will generate the
    Pandas DataFrame from these cached local files.

Script Usage
    Optional command-line parameters:

    --help, -h                  Print a usage help message and exit.
    
    --data=<DIRECTORY NAME>, -d <DIRECTORY NAME>
                                Directory for local data assets.
                                [DEFAULT: *use project assets directory*]
                                [FALLBACK: *use script directory*]"""
_citation = """\
Global Volcanism Program, 2013. Volcanoes of the World, v. 4.7.6. 
Venzke, E (ed.). Smithsonian Institution. Downloaded 02 Apr 2019. 
https://doi.org/10.5479/si.GVP.VOTW4-2013"""
_file_meta = """\
Developer: David Schenck
Project Repo: https://github.com/zero2cx/tpmc.git"""


def load_config(path):
    """When available, load project-level configuration variables.

    :param path: str
    :return: dict
    """
    try:
        sys.path.insert(0, os.path.abspath(path))
        import project
        return project.config

    except ImportError:
        return {'data_dir': '.'}

    finally:
        sys.path = sys.path[1:]


def _download_url(url):
    """Download web page at url and return its content.

    :param url: str
    :return: str
    """
    req_headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/72.0.3626.121 Safari/537.36'}
    response = requests.get(url, headers=req_headers)
    content = response.content.decode('windows-1252')

    return content


def _patch_imperfections(content):
    """Replace problematic characters in content and return it.

    :param content: str
    :return: str
    """
    content = content.replace('(<', '(lt ').replace('(lt  ', '(lt ')
    content = content.replace('(>', '(gt ').replace('(gt  ', '(gt ')

    return content


def _write_asset_file(directory, filename, content):
    """Save content to file and path.

    :param directory: str
    :param filename: str
    :param content: str
    :return: None
    """
    with open(f'{directory}/{filename}', 'w') as outfile:
        outfile.write(content)


def _generate_asset_files(directory, filenames):
    """Fetch two asset files, patch formatting errors, and save files locally.

    :param directory: str
    :param filenames: list
    :return: None
    """
    urls = ['https://volcano.si.edu/database/list_volcano_holocene_excel.cfm',
            'https://volcano.si.edu/database/list_volcano_pleistocene_excel.cfm']

    os.makedirs(directory, exist_ok=True)

    for filename, url in zip(filenames, urls):
        content = _download_url(url)
        content = _patch_imperfections(content)
        _write_asset_file(directory, filename, content)


def _locate_asset_files(directory, filenames):
    """Determine whether asset files exist locally, return boolean value.

    :param directory: str
    :param filenames: list
    :return: bool
    """
    found = []

    for filename in filenames:
        found.append(os.path.isfile(f'{directory}/{filename}'))

    return all(found)


def _fill_dead_cells(dataframe):
    """Fill all empty cells in dataframe with 'no-data' string value.

    :param dataframe: pandas.DataFrame
    :return: pandas.DataFrame
    """
    for column_name in dataframe.columns:
        dataframe[column_name] = dataframe[column_name].replace('', 'no-data')

    return dataframe


def _add_new_column(dataframe, name, content):
    """Add new column of cells to dataframe with each cell containing content.

    :param dataframe: pandas.DataFrame
    :param name: str
    :param content: str
    :return: pandas.DataFrame
    """
    dataframe[name] = [content] * len(dataframe)

    return dataframe


def _parse_asset_files(directory, filenames):
    """Create a dataframe from records contained in asset files, and return it.

    :param directory: str
    :param filenames: list
    :return: pandas.DataFrame
    """
    new_columns = [{'Epoch': 'Holocene', 'Data Status': 'Accepted'},
                   {'Epoch': 'Pleistocene', 'Data Status': 'Preliminary'}]

    dataframe = pd.DataFrame()

    for filename, new_column in zip(filenames, new_columns):
        parser = ExcelXMLHandler()
        xml.sax.parse(f'{directory}/{filename}', parser)
        new_dataframe = pd.DataFrame(parser.tables[0][2:], columns=parser.tables[0][1])
        new_dataframe = _fill_dead_cells(new_dataframe)
        for column_name, cell_data in new_column.items():
            new_dataframe = _add_new_column(new_dataframe, column_name, cell_data)
        dataframe = dataframe.append(new_dataframe, ignore_index=True)

    return dataframe


def _remove_asset_files(directory, filenames):
    """If found, delete asset files from directory.

    :param directory: str
    :param filenames: str
    :return: None
    """
    for filename in filenames:
        os.remove(f'{directory}/{filename}')


def load_dataframe(data_dir=None, force_download=False):
    """Generate dataframe from asset files, and return it.

    :param data_dir: str
    :param force_download: bool
    :return: pandas.DataFrame
    """
    if not data_dir:
        data_dir = default_data_directory

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
    """Parse and validate command line arguments.

    Return either the parsed data directory name or '.'.

    Upon request or when the parsed arguments are incoherent, print
    the module's docstring and exit.

    :param args: list
    :return: str
    """
    if not args:
        return default_data_dir

    if args[0] == '-h' or args[0] == '--help':
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


_config = load_config('..')
default_data_dir = _config['data_dir']

if __name__ == '__main__':
    import sys

    _data_dir = _parse_args(args=sys.argv[1:])
    dataframe = load_dataframe(data_dir=_data_dir)

    print(dataframe)
