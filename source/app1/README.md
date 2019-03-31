### The Python Mega Course

#### Application 1: Interactive Dictionary

Interactive Dictionary Lookup Utility

An interactive dictionary command-line script. Look up usages of a word
within a language dictionary file.
 
This project comes packaged with an English-language dictionary file.
That json-formatted data file will be used by default if no other
dictionary source is specified via the --file option.   

Optional command-line parameters:

    --help, -h                Print this help message and exit.
    --file filename, -f filename
                              Path to a json-formatted dictionary file."""
    
This script can be implemented as a standard Python module:

    >>> import source.app1.interactive_dictionary as id
    
    >>> data = id.get_data_file(filename='https://raw.githubusercontent.com/adambom/dictionary/master/dictionary.json')
    ('GIRAFFE', 'An African ruminant (Camelopardalis giraffa) related to thedeers and antelopes, but placed in a family by itself; thecamelopard. It is the tallest of animals, being sometimes twenty feetfrom the hoofs to the top of the head. Its neck is very long, and itsfore legs are much longer than its hind legs.')

    >>> id.get_near_matches(data, 'foo')
    ['FOOT', 'FOOL', 'FOOD']
    
    >>> data = id.get_data_file(filename='assets/data.json')
    
    >>> id.lookup_usages(data, 'giraffe')
    ('giraffe', ['An African even-toed ungulate mammal, the tallest of all land-living animal species.']) 
    
    >>> id.get_near_matches(data, 'foo')
    ['foot', 'fool', 'food', 'OOP', 'FOLDOC', 'Forro', 'Foodo', 'zoo']
    
    
repo | https://github.com/zero2cx/tpmc
--- | --- 
author | David Schenck
version | 1.0.4

Adapted from the Application 1 exercise:<br>
 &nbsp; &nbsp; The Python Mega Course, https://www.udemy.com/the-python-mega-course<br>
 &nbsp; &nbsp; Course creator: Ardit Sulce, https://www.udemy.com/user/adiune<br>
