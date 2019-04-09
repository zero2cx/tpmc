

########################################
`The Python Mega Course`_
########################################


============================================================
Application 2, Create Webmaps with Python and Folium
============================================================


`Webmap Generator`_
++++++++++++++++++++++++++++++++++++++++


Objective
    Generate an interactive world map featuring two data-driven
    overlays.

Detail
    The script uses two datasets while generating the map. One
    dataset contains world population data. The other dataset
    details volcano sites around the world.

    - Population by Country (2005 data), assign a color code to
      each country determined by comparison with three population
      thresholds.
    - Volcanoes of the World (GVP data), place map markers at all
      sites around the world that show or have shown volcanic
      activity. GVP refers to the Global Volcanism Program.

Script Usage
    Optional command-line parameters:

    --help, -h                  Print a usage help message and exit.

    --data=<DIRECTORY NAME>, -d <DIRECTORY NAME>
                                Directory to use for local data assets.
                                [DEFAULT: *use project assets directory*]
                                [FALLBACK: *use script directory*]

    --save=<DIRECTORY NAME>, -s <DIRECTORY NAME>
                                Save directory for the webmap.html file.
                                [DEFAULT: *use script directory*]

Module Usage
    **Place holder text.**

More Info
    Please visit the website for the `Global Volcanism Program`_ (GVP)
    for more information about the "Volcanoes of the World" database.


:Project Repo:
    https://github.com/zero2cx/tpmc

:Author:
    David Schenck, aka zero2cx

:App Version:
    0.9.3

:Acknowledgment:
    This project is forked from the Application 2 exercise of
    `The Python Mega Course`_ created by `Ardit Sulce`_.


----------------------------------------


`GVP Volcanoes Dataset Generator`_
++++++++++++++++++++++++++++++++++++++++


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

Module Usage
    **Place holder text.**

Notes
    Holocene data records are accepted as academically vetted, per
    consensus. Pleistocene data records are classified as provisional.
    Volcanoes of the World data is free to use [`GVP2019`_] thanks to
    The Smithsonian Institute's `Global Volcanism Program`_ (GVP).

.. _GVP2019:

Citation
    Data source: Global Volcanism Program, 2013. Volcanoes of the
    World, v. 4.7.6. Venzke, E (ed.). Smithsonian Institution.
    https://doi.org/10.5479/si.GVP.VOTW4-2013


.. _Webmap Generator: https://github.com/zero2cx/tpmc/blob/master/source/app2/webmap.py
.. _The Python Mega Course: https://www.udemy.com/the-python-mega-course
.. _Ardit Sulce: https://www.udemy.com/user/adiune
.. _GVP Volcanoes Dataset Generator: https://github.com/zero2cx/tpmc/blob/master/source/app2/gvp_volcanoes.py
.. _Global Volcanism Program: https://volcano.si.edu/
