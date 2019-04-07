import requests
import json
import difflib

__doc__ = """\
Interactive Dictionary Lookup Utility

An interactive dictionary command-line script. Look up usages of a word
within a language dictionary file.
 
This project comes packaged with an English-language dictionary file.
That json-formatted data file will be used by default if no other
dictionary source is specified via the --file option.   

Optional command-line parameters:

    --help, -h          Print this help message and exit.
    --file=<FILENAME>, -f <FILENAME>
                        Path to a json-formatted dictionary file."""
_disclaimer = """\
Adapted from the Application 1 exercise:
The Python Mega Course, <https://www.udemy.com/the-python-mega-course>
Course creator, Ardit Sulce <https://www.udemy.com/user/adiune>"""
_repo = 'https://github.com/zero2cx/tpmc'
_author = 'David Schenck, aka zero2cx'
__version__ = '1.0.5'


class DownloadError(Exception):
    pass


class InvalidFileStructure(Exception):
    pass


def get_data_file(filename):
    """Read the specified json-formatted file containing common word usages.

    Populate and return a dict containing words (keys) and their dictionary
    usages (values).

    The language dictionary file must contain a valid json structure. The
    file may be located on the local filesystem or on a remote server.

    :param filename:        string of source file name
    :return:                dict of parsed data from json-formatted file
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
    """Lookup dictionary usages for the specified word.

    Return a 2-tuple consisting of either: the validated word and a list
    containing all word usages that were found, or the unvalidated word
    and None in those cases where no usages were found.

    :param data:            dict repository of word usages
    :param word:            string of word to look up
    :return:                2-tuple of (word, list of usages) or (word, None)
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
    """Locate the best dictionary near-matches for the specified word.

    Use the difflib package to find the best near-matches for the word.

    :param data:            dict repository of word usages
    :param word:            string of word to near-match
    :return:                list of near-match words that were found
    """
    guess_words = [word.lower(), word.upper(), word.title()]
    words = []

    for guess_word in guess_words:
        words.extend(difflib.get_close_matches(guess_word, data.keys()))

    return words


def _parse_args(args):
    """Parse and validate any command line arguments.

    Return either the parsed or default dictionary file name.

    Upon request or when the parsed arguments are incoherent, print the
    module's docstring and exit.

    :param args:            list of command-line arguments
    :return:                string of dictionary file name
    """
    project_root = '../..'
    default_assets_dir = 'assets/data'
    default_data_file = 'data.json'

    if not args:
        return f'{project_root}/{default_assets_dir}/{default_data_file}'

    if  args[0] == '-h' or args[0] == '--help':
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
    """The main loop implements a command-line prompt interface for user input.

    Prompt the user for a word, conduct a dictionary lookup, print the result,
    then loop. Terminate the loop when the user elects to quit.

    :param data:            dict repository of word usages
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


if __name__ == '__main__':
    import sys
    dictionary_filename = _parse_args(args=sys.argv[1:])
    dictionary_data = get_data_file(filename=dictionary_filename)
    _main(data=dictionary_data)
