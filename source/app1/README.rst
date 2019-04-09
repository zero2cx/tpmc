

########################################
`The Python Mega Course`_
########################################


========================================
Application 1: Interactive Dictionary
========================================


`Interactive Dictionary Lookup Utility`_
++++++++++++++++++++++++++++++++++++++++

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
                                Path to a json-formatted dictionary file.

Module Usage
    ::

        >>> import interactive_dictionary as id

        >>> data = id.get_data_file(filename='assets/data.json')

        >>> id.lookup_usages(data, 'giraffe')   # lookup the word "giraffe"
        ('giraffe', ['An African even-toed ungulate mammal, the tallest of all land-living animal species.'])

        >>> id.get_near_matches(data, 'foo')    # find nearest matches for the word "foo"
        ['foot', 'fool', 'food', 'OOP', 'FOLDOC', 'Forro', 'Foodo', 'zoo']

        >>> data = id.get_data_file(filename='https://raw.githubusercontent.com/adambom/dictionary/master/dictionary.json')

        >>> id.lookup_usages(data, 'giraffe')   # lookup the word "giraffe"
        ('GIRAFFE', 'An African ruminant (Camelopardalis giraffa) related to thedeers and antelopes, but placed in a family by itself; thecamelopard. It is the tallest of animals, being sometimes twenty feetfrom the hoofs to the top of the head. Its neck is very long, and itsfore legs are much longer than its hind legs.')

        >>> id.get_near_matches(data, 'foo')    # find nearest matches for the word "foo"
        ['FOOT', 'FOOL', 'FOOD']


:Project Repo:
    https://github.com/zero2cx/tpmc.git

:Author:
    David Schenck

:App Version:
    1.0.5

:Acknowledgment:
    This project is forked from the Application 1 exercise of
    `The Python Mega Course`_ (creator: `Ardit Sulce`_).


.. _The Python Mega Course: https://www.udemy.com/the-python-mega-course
.. _Ardit Sulce: https://www.udemy.com/user/adiune
.. _Interactive Dictionary Lookup Utility: https://github.com/zero2cx/tpmc/blob/master/source/app1/interactive_dictionary.py
