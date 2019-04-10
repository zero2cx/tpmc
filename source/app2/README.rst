

########################################
`The Python Mega Course`_
########################################


============================================================
Application 2: Create Webmaps with Python and Folium
============================================================


`Webmap Generator`_
++++++++++++++++++++++++++++++++++++++++


Objective
  Generate an interactive map of the world featuring two
  toggleable map overlays.

Script Usage
  Optional command-line parameters:

  --help, -h                  Print a usage help message and exit.

  --data=<DIRECTORY NAME>, -d <DIRECTORY NAME>
                              Directory to use for local data assets.
                              [DEFAULT: *use project assets directory*]
                              [FALLBACK: *use script directory*]

  --save=<DIRECTORY NAME>, -s <DIRECTORY NAME>
                              Save directory for the webmap file.
                              [DEFAULT: *use script directory*]

Module Usage
    ::

        >>> import webmap as wm

        >>> my_map = wm.generate_webmap(data_dir='.')               # data_dir: specify location of file world.json

        >>> my_map
        <folium.folium.Map at 0x516e550>

        >>> wm.write_webmap(webmap=my_map, file='./my_map.html')    # file: specify directory and file name to write

    After the example shown above, the generated file *my_map.html*
    is viewable in any modern web browser.

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

More Info
    Please visit the website for the `Global Volcanism Program (GVP)`_
    for more information about the "Volcanoes of the World" database.


:Project Repo:
    https://github.com/zero2cx/tpmc.git

:Author:
    David Schenck

:App Version:
    1.0.1

:Acknowledgment:
    This app is forked from the Application 2 exercise of
    `The Python Mega Course`_ (creator: `Ardit Sulce`_).


----------------------------------------


`GVP Volcanoes Dataset Generator`_
++++++++++++++++++++++++++++++++++++++++


Objective
    Generate a dataset of all catalogued geologic sites worldwide which
    exhibit evidence of past or present volcanic activity.

Script Usage
    Optional command-line parameters:

    --help, -h                  Print a usage help message and exit.

    --data=<DIRECTORY NAME>, -d <DIRECTORY NAME>
                                Directory to use for local data assets.
                                [DEFAULT: *use the script directory*]

Module Usage
    ::

        >>>

        >>>

        >>>

        >>>

Detail
    The initial step is to download and/or parse two Microsoft Excel
    XML-format dataset files. Then minor format issues in the data are
    patched. Finally, the records from each file are processed and
    combined into one Pandas DataFrame.

Data Caching
    The Dataset Generator's initial execution will download the GVP's
    latest dataset files. Minor format imperfections in the records are
    then cleaned up. These cleaned-up files are cache-stored in the
    local filesystem. Second-run script executions will generate the
    Pandas DataFrame from these cached local files.

Notes
    Holocene data records are accepted as academically vetted, per
    consensus. Pleistocene data records are classified as provisional.
    Volcanoes of the World data is free to use thanks to The
    Smithsonian Institute's `Global Volcanism Program (GVP)`_.

Citation
    Data source: Global Volcanism Program, 2013. Volcanoes of the
    World, v. 4.7.6. Venzke, E (ed.). Smithsonian Institution.
    https://doi.org/10.5479/si.GVP.VOTW4-2013


.. _The Python Mega Course: https://www.udemy.com/the-python-mega-course
.. _Ardit Sulce: https://www.udemy.com/user/adiune
.. _Webmap Generator: https://github.com/zero2cx/tpmc/blob/master/source/app2/webmap.py
.. _GVP Volcanoes Dataset Generator: https://github.com/zero2cx/tpmc/blob/master/source/app2/gvp_volcanoes.py
.. _Global Volcanism Program (GVP): https://volcano.si.edu/
