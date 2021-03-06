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
    That json-formatted data file will be used by default (when
    present) if no other dictionary source is specified using
    the --file option.

    Example dictionary files can be viewed or downloaded from
    these urls:

    - https://raw.githubusercontent.com/zero2cx/tpmc/master/assets/data/data.json

    - https://raw.githubusercontent.com/adambom/dictionary/master/dictionary.json

    For any other dictionary file, an acceptable json structure
    should be one of these:

    - { "WORD": "DEFINITION", ... }

    - { "WORD": [ "DEFINITION_1", "DEFINITION_2", ... ], ... }

Script Usage
    Optional command-line parameters:

    --help, -h                  Print this help message and exit.

    --file=<PATH TO FILE>, -f <PATH TO FILE>
                                Path to a json-formatted dictionary file."""
_file_meta = """\
Project Repo: https://github.com/zero2cx/tpmc.git
Author: David Schenck
Acknowledgement: This app is forked from the Application 1 exercise of
`The Python Mega Course`_ https://www.udemy.com/the-python-mega-course
(creator: `Ardit Sulce`_ https://www.udemy.com/user/adiune)."""
_path_to_project_module = '..'


class DownloadError(Exception):
    pass


class InvalidFileStructure(Exception):
    pass


def _load_from_config(path):
    """When available, load project-level config variables.

    :param path: str
    :return: str
    """
    try:
        sys.path.insert(0, os.path.abspath(path))
        import config
        return config.data_dir

    except ImportError:
        return '.'

    finally:
        sys.path = sys.path[1:]


def _parse_args(args):
    """Parse and validate command line arguments.

    Return either the parsed or default dictionary file name.

    Upon request or when the parsed arguments are incoherent, print the
    module's docstring and exit.

    :param args: list
    :return: str
    """
    if not args:
        return f'{_data_dir}/data.json'

    if '--help' in args or '-h' in args:
        print(__doc__)
        exit(0)

    if args[0][:7] == '--file=':
        path_to_file = args[0][7:]
        if path_to_file == '':
            print(__doc__)
            exit(1)
        return path_to_file

    if args[0] == '-f':
        try:
            return args[1]
        except IndexError:
            print(__doc__)
            exit(1)


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
        found_word, found_usages = find_word(data, word)

        if isinstance(found_usages, list):
            print(f'  [SUCCESS] found {len(found_usages)} usages of {found_word}:')
            for usage in found_usages:
                print(f'    * {usage}')

        elif isinstance(found_usages, str):
            print(f'  [SUCCESS] found 1 usage of {found_word}')
            print(f'    * {found_usages}')

        else:
            print(f'  [FAILURE] {word} not found', end='')
            found_near_matches = find_near_matches(data, word)

            if found_near_matches:
                print(f'... did you mean?')
                for near_match in found_near_matches:
                    print(f'    ? {near_match}')
            else:
                print()

        word = input(f'\n{prompt_msg}').strip()

    else:
        print('!! Finished !!')


def find_near_matches(data, word):
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


def find_word(data, word):
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


def load_data_file(file='data.json'):
    """Read json-formatted file containing common words and their usages.

    Populate and return a dict containing words (keys) and their
    dictionary usages (values).

    The language dictionary file must read as a valid json structure.
    The file may be located either on the local filesystem or on a
    remote server.

    :param file: str
    :return: dict
    """
    try:
        with open(file) as fh:
            return json.loads(fh.read())

    except FileNotFoundError:
        raise FileNotFoundError(file)

    except json.JSONDecodeError:
        raise InvalidFileStructure(file)

    except OSError as e:
        if e.strerror == 'Invalid argument' and file[:4] == 'http':
            try:
                req = requests.get(file)
                return json.loads(req.content)

            except requests.exceptions.RequestException:
                raise DownloadError(file)

            except json.JSONDecodeError:
                raise InvalidFileStructure(file)

        raise FileNotFoundError(file)


_data_dir = _load_from_config(path=_path_to_project_module)

if __name__ == '__main__':
    file = _parse_args(args=sys.argv[1:])
    data = load_data_file(file=file)
    _main(data=data)
