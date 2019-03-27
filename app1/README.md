### The Python Mega Course

#### Application 1: Interactive Dictionary

Interactive Dictionary Lookup Utility

An interactive dictionary command-line script. Look up usages of a word
within a common-language dictionary file.
 
This project comes packaged with an English-language dictionary file.
That json-formatted data file will be used by default if no other
dictionary source is specified (see below).   

Optional command-line parameters:

    --help, -h                  Print this help message and exit.
    --file string, -f string    Path to a json-formatted dictionary file.
    
This script can be implemented as a standard Python module:

    >>> import app1.interactive_dictionary as id
    
    >>> data = id.get_data_file(filename='assets/data.json')
    
    >>> id.main(data=data)
        <...>
        
    >>> data = id.get_data_file(filename='https://raw.githubusercontent.com/adambom/dictionary/master/dictionary.json')
    
    >>> id.main(data=data)
        <...>

repo | https://github.com/zero2cx/tpmc
--- | --- 
version | 1.0.1
author | David Schenck

Adapted from the Application 1 exercise:<br>
 &nbsp; &nbsp; The Python Mega Course, https://www.udemy.com/the-python-mega-course<br>
 &nbsp; &nbsp; Course instructor: Ardit Sulce, https://www.udemy.com/user/adiune<br>
