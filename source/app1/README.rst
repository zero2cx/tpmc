

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
                                Path to a json-formatted dictionary file.

Module Usage
    ::

        >>> import interactive_dictionary as id

        >>> # FIRST, LOAD DICTIONARY WORDS FROM A LOCALLY SAVED FILE
        ...

        >>> data = id.load_data_file('../../assets/data/data.json')

        >>> id.find_word(data, 'foo')
        ('foo', None)

        >>> id.find_near_matches(data, 'foo')
        ['foot', 'fool', 'food', 'OOP', 'FOLDOC', 'Forro', 'Foodo', 'zoo']

        >>> id.find_word(data, 'bar')
        ('bar', ['A business licensed to sell intoxicating beverages for
        consumption on the premises, or the premises themselves', 'With the
        exception of.', 'A musical designation consisting of all notes and
        or rests delineated by two vertical bars; an equal and regular
        division of the whole of a composition.', 'A unit of pressure equal
        to 100,000 pascals.', 'To render passage impossible by physical
        obstruction.', 'A rigid piece of metal or wood, usually used as a
        fastening or obstruction or weapon.', 'To accept no longer in a
        community, group or country, e.g. by official decree.', 'To prevent
        from entering; to keep out (e.g. of membership).', 'A single piece
        of a grid, railing, grating, pailing, fence, etc.', 'A block of
        solid substance (such as soap, wax or chocolate).', 'A horizontal
        rod used by gymnasts as a support to perform their physical
        exercises.', 'A counter where you can obtain food or drink.', 'An
        obstruction (usually metal) placed at the top of a goal.'])

        >>> id.find_near_matches(data, 'bar')
        ['bar', 'boar', 'bear', 'BA', 'AR', 'FAR', 'Baré', 'Bari', 'Bara']

        >>> # NEXT, LOAD DICTIONARY WORDS FROM A URL ON A REMOTE SERVER
        ...

        >>> data = id.load_data_file('https://raw.githubusercontent.com/ada
        mbom/dictionary/master/dictionary.json')

        >>> id.find_word(data, 'foo')
        ('foo', None)

        >>> id.find_near_matches(data, 'foo')
        ['FOOT', 'FOOL', 'FOOD']

        >>> id.find_word(data, 'bar')
        ('BAR', 'An ordinary, like a fess but narrower, occupying only one
        fifthpart of the field.')

        >>> id.find_near_matches(data, 'bar')
        ['BAR', 'BOAR', 'BEAR']


:Project Repo:
    https://github.com/zero2cx/tpmc.git

:Author:
    David Schenck

:App Version:
    1.0.6

:Acknowledgment:
    This project is forked from the Application 1 exercise of
    `The Python Mega Course`_ (creator: `Ardit Sulce`_).


.. _The Python Mega Course: https://www.udemy.com/the-python-mega-course
.. _Ardit Sulce: https://www.udemy.com/user/adiune
.. _Interactive Dictionary Lookup Utility: https://github.com/zero2cx/tpmc/blob/master/source/app1/interactive_dictionary.py
