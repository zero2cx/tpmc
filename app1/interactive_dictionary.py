import json
import difflib

__doc__ = """Interactive Dictionary Lookup Utility

An interactive dictionary, word usage lookup command-line script.

Optional command-line parameters:
    --help, -h                  Print this help message and exit.
    --file string, -f string    Path to a json-formatted dictionary file.
"""
_author = 'David Schenck, aka zero2cx'
_repo = 'https://github.com/zero2cx/tpmc'
_disclaimer = """Code adapted from the App1 exercise of:
  The Python Mega Course, <https://www.udemy.com/the-python-mega-course>
  Course instructor, Ardit Sulce <https://www.udemy.com/user/adiune> 
"""


def _lookup_usages(data, word):
    """If possible, lookup valid usages for the specified word.

    Return the validated word and any word usages that are found within the
    global dict (i.e. data), or the unvalidated word and None.

    :param data:        [dict]  repository of word usages
    :param word:        [str]   word to look up
    :return:            [tuple] (word with case as found, list of usages) or
                                (word with original case, None)
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


def _get_near_misses(data, word):
    """Use difflib to try to locate any close matches for the specified word.

    :param data:        [dict]  repository of word usages
    :param word:        [str]   word to match via difflib
    :return:            [set]   close matches that were found
    """
    guess_words = [word.lower(), word.upper(), word.title()]
    words = []

    for guess_word in guess_words:
        words.extend(difflib.get_close_matches(guess_word, data.keys()))

    return set(words)


def _parse_args(args):
    """Parse and validate any command line arguments.

    Upon request or if arguments are incoherent, print the module docstring
    and exit. Return the parsed or default dictionary file name.

    :param args:    [list]  command-line arguments
    :return:        [str]   parsed or default dictionary file name
    """
    default_assets_dir = '../assets'
    default_data_file = 'data.json'

    if not args:
        return f'{default_assets_dir}/{default_data_file}'

    if args[0] == '--help' or args[0] == '-h':
        print(__doc__)
        exit(0)

    if args[0] == '--file' or args[0] == '-f':
        try:
            return args[1]
        except:
            print(__doc__)
            exit(1)


def _get_data(filename):
    """Read the specified json-formatted file containing common word usages.

    Populate and return a dict containing dictionary word usage data.

    :param filename:    [str]   source file name
    :return:            [dict]  parsed content from json-formatted source file
    """
    with open(filename) as fh:
        return json.loads(fh.read())


def _main(data):
    """Main loop that prompts for a word, produces the result, and prints it.

    :param data:        [dict]  repository of word usages
    """
    banner_msg = '== Interactive Dictionary Lookup Utility =='
    prompt_msg = 'Type a word [hit ENTER to quit]: '
    word = input(f'{banner_msg}\n{prompt_msg}').strip()

    while word:
        found_word, found_usages = _lookup_usages(data, word)

        if found_usages:
            print(f'** found {len(found_usages)} usages of {found_word} **')
            for usage in found_usages:
                print(f'   * {usage}')

        else:
            print(f'-- word not found: {word} --')
            found_words = _get_near_misses(data, word)

            if found_words:
                print(f'?? did you mean ??')
                for found_word in found_words:
                    print(f'   ? {found_word}')

        word = input(f'\n{prompt_msg}').strip()

    else:
        print('!! Finished !!')


if __name__ == '__main__':
    import sys
    _main(_get_data(_parse_args(sys.argv[1:])))
