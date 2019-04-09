import os
import sys
import requests
import json
import difflib

__doc__ = """\
Interactive Dictionary Lookup Utility

Objective
    Look up usages of a word within a language dictionary file.

Detail
    This is an interactive dictionary command-line script. This
    app comes packaged with an English-language dictionary file.
    That json-formatted data file will be used by default if no
    other dictionary source is specified via the --file option.
    Json format should be one of these:

    - { "WORD": "DEFINITION", ... }
    
    - { "WORD": [ "DEFINITION_1", "DEFINITION_2", ... ], ... }

Script Usage
    Optional command-line parameters:

    --help, -h                  Print this help message and exit.

    --file=<PATH TO FILE>, -f <PATH TO FILE>
                                Path to a json-formatted dictionary file."""
_file_meta = """\
Developer: David Schenck
Project Repo: https://github.com/zero2cx/tpmc.git
Disclaimer: This project is forked from the Application 1 exercise of
`The Python Mega Course`_ https://www.udemy.com/the-python-mega-course
(creator: `Ardit Sulce`_ https://www.udemy.com/user/adiune)."""


class DownloadError(Exception):
    pass


class InvalidFileStructure(Exception):
    pass


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


def get_data_file(filename):
    """Read json-formatted file containing common words and their usages.

    Populate and return a dict containing words (keys) and their
    dictionary usages (values).

    The language dictionary file must read as a valid json structure.
    The file may be located either on the local filesystem or on a
    remote server.

    :param filename: str
    :return: dict
    """
    try:
        with open(filename) as fh:
            return json.loads(fh.read())

    except FileNotFoundError:
        raise FileNotFoundError(filename)

    except json.JSONDecodeError:
        raise InvalidFileStructure(filename)

    except OSError as e:
        if e.strerror == 'Invalid argument' and filename[:4] == 'http':
            try:
                req = requests.get(filename)
                return json.loads(req.content)

            except requests.exceptions.RequestException:
                raise DownloadError(filename)

            except json.JSONDecodeError:
                raise InvalidFileStructure(filename)

        raise FileNotFoundError(filename)


def lookup_usages(data, word):
    """Look up usages for word within data.

    Return a 2-tuple of either: a) the validated word and
    the list containing all word usages that are found, or
    b) the unvalidated word and None for those cases where
    no usages are found.

    :param data: dict
    :param word: str
    :return: tuple
    """
    usages = data.get(word.lower())
    if usages:
        return word.lower(), usages

    usages = data.get(word.upper())
    if usages:
        return word.upper(), usages

    usages = data.get(word.title())
    if usages:
        return word.title(), usages

    return word, None


def get_near_matches(data, word):
    """Locate best near-matches for word within data.

    Use the difflib package to find the best near-matches for this word.

    :param data: dict
    :param word: str
    :return: list
    """
    guess_words = [word.lower(), word.upper(), word.title()]
    words = []

    for guess_word in guess_words:
        words.extend(difflib.get_close_matches(guess_word, data.keys()))

    return words


def _parse_args(args):
    """Parse and validate command line arguments.

    Return either the parsed or default dictionary file name.

    Upon request or when the parsed arguments are incoherent, print the
    module's docstring and exit.

    :param args: list
    :return: str
    """
    project_root = '../..'
    default_assets_dir = 'assets/data'
    default_data_file = 'data.json'

    if not args:
        return f'{project_root}/{default_assets_dir}/{default_data_file}'

    if args[0] == '-h' or args[0] == '--help':
        print(__doc__)
        exit(0)

    if args[0] == '-f':
        try:
            return args[1]
        except IndexError:
            print(__doc__)
            exit(1)

    if args[0][:7] == '--file=':
        file = args[0][7:]
        if file == '':
            print(__doc__)
            exit(1)
        return file


def _main(data):
    """Use looping user-prompt interface to query user for keyboard input.

    Prompt the user for a word, conduct a dictionary lookup, print the result,
    then loop. Terminate the loop when the user elects to quit.

    :param data: dict
    :return: None
    """
    banner_msg = '== Interactive Dictionary Lookup Utility =='
    prompt_msg = 'Type a word [hit ENTER to quit]: '
    word = input(f'{banner_msg}\n{prompt_msg}').strip()

    while word:
        found_word, found_usages = lookup_usages(data, word)

        if isinstance(found_usages, list):
            print(f'  * found {len(found_usages)} usages of {found_word}')
            for usage in found_usages:
                print(f'    * {usage}')

        elif isinstance(found_usages, str):
            print(f'  * found 1 usage of {found_word}')
            print(f'    * {found_usages}')

        else:
            print(f'  - {word} not found', end='')
            found_misses = get_near_matches(data, word)

            if found_misses:
                print(f'... did you mean?')
                for found_miss in found_misses:
                    print(f'    ? {found_miss}')
            else:
                print()

        word = input(f'\n{prompt_msg}').strip()

    else:
        print('!! Finished !!')


_config = load_config('..')
default_data_dir = _config['data_dir']

if __name__ == '__main__':
    dictionary_filename = _parse_args(args=sys.argv[1:])
    dictionary_data = get_data_file(filename=dictionary_filename)
    _main(data=dictionary_data)
