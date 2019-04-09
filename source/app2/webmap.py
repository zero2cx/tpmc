import os
import sys
import folium
import gvp_volcanoes as gvp

__doc__ = """\
Webmap Generator

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
      activity.

Script Usage
    Optional command-line parameters:

    --help, -h                  Print a usage help message and exit.

    --data=<DIRECTORY NAME>, -d <DIRECTORY NAME>
                                Directory to use for local data assets.
                                [DEFAULT: *use project assets directory*]
                                [FALLBACK: *use script directory*]

    --save=<DIRECTORY NAME>, -s <DIRECTORY NAME>
                                Save directory for the webmap.html file.
                                [DEFAULT: *use script directory*]"""
_file_meta = """\
Developer: David Schenck
Project Repo: https://github.com/zero2cx/tpmc.git
Disclaimer: This project is forked from the Application 2 exercise of
`The Python Mega Course`_ https://www.udemy.com/the-python-mega-course
(creator: `Ardit Sulce`_ https://www.udemy.com/user/adiune)."""


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


def _generate_color_string(elevation):
    """Determine appropriate color-string based on elevation, and return it.

    :param elevation: string
    :return: string
    """
    """List of valid Marker colors:
    red, darkred, lightred, orange, beige, green, darkgreen, lightgreen,
    blue, darkblue, lightblue, cadetblue, purple, darkpurple, pink,
    white, gray, lightgray, black"""
    try:
        elevation = int(elevation)
    except ValueError:
        elevation = 0

    if elevation < 0:
        return 'beige'

    elif 0 <= elevation < 500:
        return 'lightgray'

    elif 500 <= elevation < 1000:
        return 'pink'

    elif 1000 <= elevation < 1500:
        return 'orange'

    elif 1500 <= elevation < 2000:
        return 'green'

    elif 2000 <= elevation < 2500:
        return 'blue'

    elif 2500 <= elevation < 3000:
        return 'purple'

    elif 3000 <= elevation < 4000:
        return 'darkred'

    else:
        return 'red'


def _generate_popup(name, elev, detail_url, height, width,
                    embed_url, bbox, layer_type):
    """Generate html iframe, add a caption, and return it.

    :param name: string
    :param elev: string
    :param detail_url: string
    :param height: string
    :param width: string
    :param embed_url: string
    :param bbox: string
    :param layer_type: string
    :return: string
    """
    popup_caption = f"""\
        <strong style="float: left;">{name} ({elev}m)</strong>
        <em style="float: right;"><a href="{detail_url}" target="_blank" 
          rel="noopener noreferrer">Site detail</a></em><br/>"""
    popup = f"""\
        <iframe frameborder="0" scrolling="no" style="border: 1px solid black"
          height="{height}" width="{width}" marginheight="0" marginwidth="0"
          src="{embed_url}?bbox={bbox}&amp;layer={layer_type}"></iframe><br/>
        {popup_caption}"""

    return popup


def _generate_volcano_layer(nums, names, elevs, lats, lons):
    """Generate "Volcanoes of the World" FeatureGroup layer, and return it.

    :param nums: list
    :param names: list
    :param elevs: list
    :param lats: list
    :param lons: list
    :return: pandas.FeatureGroup
    """
    embed_url = 'https://www.openstreetmap.org/export/embed.html'
    height = '200'
    width = '400'
    layer_type = 'cyclemap'
    lat_diff = 0.088
    lon_diff = 0.160
    fgv = folium.FeatureGroup(name="Volcanoes of the World (via GVP)")

    for num, name, elev, lat, lon in zip(nums, names, elevs, lats, lons):
        lat = float(lat)
        lon = float(lon)
        fill_color = _generate_color_string(elev)
        tooltip = f'{name} ({elev}m)'

        bbox = f'{lon-lon_diff}%2C{lat-lat_diff}%2C{lon+lon_diff}%2C{lat+lat_diff}'
        detail_url = f'https://volcano.si.edu/volcano.cfm?vn={num}&vtab=GeneralInfo'
        popup = _generate_popup(name, elev, detail_url, height, width,
                                embed_url, bbox, layer_type)

        fgv.add_child(folium.RegularPolygonMarker(
            location=[lat, lon], color='white', radius=10, weight=1,
            number_of_sides=3, rotation=30, fill_opacity=0.7,
            fill_color=fill_color, tooltip=tooltip, popup=popup))

    return fgv


def _parse_volcano_data(dataframe):
    """Parse columns of data from dataframe, and return them as tuple.

    :param dataframe: pandas.DataFrame
    :return: tuple
    """
    numbers = list(dataframe["Volcano Number"])
    names = list(dataframe["Volcano Name"])
    elevations = list(dataframe["Elevation (m)"])
    latitudes = list(dataframe["Latitude"])
    longitudes = list(dataframe["Longitude"])

    return numbers, names, elevations, latitudes, longitudes


def _generate_population_layer(filename):
    """Generate "Population by Country" FeatureGroup layer and return it.

    :return: folium.FeatureGroup
    """
    fgp = folium.FeatureGroup(name="Population by Country (2005 data)")

    layer = folium.GeoJson(data=open(filename, 'r', encoding='utf-8-sig').read(),
        style_function=lambda x: {'weight': 0, 'fillColor':
            'yellow' if x['properties']['POP2005'] < 10000000
            else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
            else 'red'}
    )

    fgp.add_child(layer)

    return fgp


def generate_webmap():
    """Generate a folium.Map, add two FeatureGroup layers, and return it.

    :return: folium.Map
    """
    webmap = folium.Map(location=[38.000, -99.000], tiles="Mapbox Bright")
    population_layer = _generate_population_layer('../../assets/data/world.json')
    webmap.add_child(population_layer)
    dataframe = gvp.load_dataframe()
    nums, names, elevs, lats, lons = _parse_volcano_data(dataframe)
    volcano_layer = _generate_volcano_layer(nums, names, elevs, lats, lons)
    webmap.add_child(volcano_layer)
    webmap.add_child(folium.LayerControl())

    return webmap


def save_webmap(webmap, filename):
    """Save instance of folium.Map as html file to local filesystem.

    :param webmap: folium.Map
    :param filename: string
    :return: None
    """
    webmap.save(filename)


def _parse_args(args):
    """Parse and validate command line arguments, and return parsed values.

    Return either the parsed path-to-directory string or '.'.

    Upon request or when the parsed arguments are incoherent, print
    the module's docstring and exit.

    :param args: list
    :return: string
    """
    if not args:
        return default_data_dir

    if args[0] == '--help' or args[0] == '-h':
        print(__doc__)
        exit(0)

    if args[0][:7] == '--data=':
        directory = args[0][7:]
        if directory == '':
            print(__doc__)
            exit(1)
        return directory

    if args[0] == '-d':
        try:
            return args[1]
        except IndexError:
            print(__doc__)
            exit(1)


_config = load_config('..')
default_data_dir = _config['data_dir']


if __name__ == '__main__':
    _data_path = _parse_args(args=sys.argv[1:])
    webmap_path = '/'.join(os.getcwd().split('\\'))
    filename = 'webmap.html'

    webmap = generate_webmap()
    save_webmap(webmap, f'{webmap_path}/{filename}')

    print(f'Webmap page saved to file:\n  file:///{webmap_path}/{filename}')
