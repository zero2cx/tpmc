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
                                Directory to use for local data assets.
                                [DEFAULT: *use the script directory*]

    --save=<DIRECTORY NAME>, -s <DIRECTORY NAME>
                                Directory to use to save the webmap file.
                                [DEFAULT: *use the script directory*]"""
_citation = """\
Global Volcanism Program, 2013. Volcanoes of the World, v. 4.7.6. Venzke, E (ed.).
Smithsonian Institution. https://doi.org/10.5479/si.GVP.VOTW4-2013"""
_file_meta = """\
Project Repo: https://github.com/zero2cx/tpmc.git
Author: David Schenck"""
_path_to_project_module = '..'


def _load_from_config(path):
    """When available, load project-level configuration variables.

    :param path: str
    :return: str
    """
    try:
        sys.path.insert(0, os.path.abspath(path))
        import project
        return project.data_dir

    except ImportError:
        return '.'

    finally:
        sys.path = sys.path[1:]


def _download_url(url):
    """Download web page at url.

     Return the content of the web page.

    :param url: str
    :return: str
    """
    req_headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/72.0.3626.121 Safari/537.36'}
    response = requests.get(url=url, headers=req_headers)
    content = response.content.decode(encoding='windows-1252')

    return content


def _patch_imperfections(content):
    """Replace problematic characters in content.

    Return the patched content.

    :param content: str
    :return: str
    """
    content = content.replace('(<', '(lt ').replace('(lt  ', '(lt ')
    content = content.replace('(>', '(gt ').replace('(gt  ', '(gt ')

    return content


def _write_asset_file(directory, file, content):
    """Save content to local filesystem.

    :param directory: str
    :param file: str
    :param content: str
    :return: None
    """
    with open(f'{directory}/{file}', 'w') as outfile:
        outfile.write(content)


def _generate_asset_files(directory, files):
    """Fetch the asset files, patch formatting errors, and save files locally.

    :param directory: str
    :param files: list
    :return: None
    """
    urls = ['https://volcano.si.edu/database/list_volcano_holocene_excel.cfm',
            'https://volcano.si.edu/database/list_volcano_pleistocene_excel.cfm']

    os.makedirs(directory, exist_ok=True)

    for url, file in zip(urls, files):
        content = _download_url(url=url)
        content = _patch_imperfections(content=content)
        _write_asset_file(directory=directory, file=file, content=content)


def _locate_asset_files(directory, files):
    """Determine whether asset files exist locally.

    Return one boolean value showing whether all of the files were found.

    :param directory: str
    :param files: list
    :return: bool
    """
    found = []

    for file in files:
        found.append(os.path.isfile(f'{directory}/{file}'))

    return all(found)


def _fill_dead_cells(dataframe):
    """Fill all empty cells in dataframe with 'no-data' string value.

    Return the modified DataFrame.

    :param dataframe: pandas.DataFrame
    :return: pandas.DataFrame
    """
    for column_name in dataframe.columns:
        dataframe[column_name] = dataframe[column_name].replace('', 'no-data')

    return dataframe


def _add_new_column(dataframe, name, content):
    """Add new column of cells to DataFrame with each cell containing content.

    Return the modified DataFrame.

    :param dataframe: pandas.DataFrame
    :param name: str
    :param content: str
    :return: pandas.DataFrame
    """
    dataframe[name] = [content] * len(dataframe)

    return dataframe


def _parse_asset_files(directory, files):
    """Generate DataFrame from records contained in asset files.

    Return the generated DataFrame.

    :param directory: str
    :param files: list
    :return: pandas.DataFrame
    """
    new_columns = [{'Epoch': 'Holocene', 'Data Status': 'Accepted'},
                   {'Epoch': 'Pleistocene', 'Data Status': 'Preliminary'}]

    dataframe = pd.DataFrame()

    for file, new_column in zip(files, new_columns):
        parser = ExcelXMLHandler()
        xml.sax.parse(source=f'{directory}/{file}', handler=parser)
        new_dataframe = pd.DataFrame(data=parser.tables[0][2:],
                                     columns=parser.tables[0][1])
        new_dataframe = _fill_dead_cells(dataframe=new_dataframe)
        for column_name, cell_data in new_column.items():
            new_dataframe = _add_new_column(dataframe=new_dataframe,
                                            name=column_name, content=cell_data)
        dataframe = dataframe.append(new_dataframe, ignore_index=True)

    return dataframe


def _remove_asset_files(directory, files):
    """If found, delete asset files from directory.

    :param directory: str
    :param files: list
    :return: None
    """
    for file in files:
        os.remove(f'{directory}/{file}')


def load_dataframe(data_dir=None, force_download=False):
    """Generate DataFrame from asset files.

    Return the generated DataFrame.

    :param data_dir: str
    :param force_download: bool
    :return: pandas.DataFrame
    """
    if not data_dir:
        data_dir = default_data_directory

    filenames = ['GVP_Volcano_List_Holocene-cleaned.xls',
                 'GVP_Volcano_List_Pleistocene-cleaned.xls']

    if force_download:
        _remove_asset_files(directory=data_dir, files=filenames)

    found = _locate_asset_files(directory=data_dir, files=filenames)

    if not found:
        _generate_asset_files(directory=data_dir, files=filenames)

    dataframe = _parse_asset_files(directory=data_dir, files=filenames)

    return dataframe


def _parse_args(args):
    """Parse and validate command line arguments.

####################################################################
    Return a tuple
either the parsed directory name or global _data_dir.
####################################################################

    Upon request or when the parsed arguments are incoherent, print
    the module's docstring and exit.

    :param args: list
    :return: tuple
    """
    if not args:
        return _data_dir, _save_dir

    if '--help' in args or '-h' in args:
        print(__doc__)
        exit(0)

    data_dir = _data_dir
    save_dir = _save_dir

    for i, arg in enumerate(args):

        if arg[:7] == '--data=':
            data_dir = arg[7:]
            if data_dir == '':
                print(__doc__)
                exit(1)
            continue

        if arg[:7] == '--save=':
            save_dir = arg[7:]
            if save_dir == '':
                print(__doc__)
                exit(1)
            continue

        if arg == '-d':
            args[0]
            try:
                data_dir = args.pop(0)
            except IndexError:
                print(__doc__)
                exit(1)

        if arg == '-s':
            try:
                return args[1]
            except IndexError:
                print(__doc__)
                exit(1)

        return data_dir, save_dir


_data_dir = _load_from_config(path=_path_to_project_module)
_save_dir = _data_dir

if __name__ == '__main__':
    _data_dir = _parse_args(args=sys.argv[1:])
    dataframe = load_dataframe(data_dir=_data_dir)

    print(dataframe)
