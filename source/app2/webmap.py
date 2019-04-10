import os
import sys
import folium
import gvp_volcanoes as gvp
from argparse import ArgumentParser, RawDescriptionHelpFormatter

_path_to_config = '..'
_file_meta = """\
Project Repo: https://github.com/zero2cx/tpmc.git
Author: David Schenck
Acknowledgement: This app is forked from the Application 2 exercise of
`The Python Mega Course`_ https://www.udemy.com/the-python-mega-course
(creator: `Ardit Sulce`_ https://www.udemy.com/user/adiune)."""
_description = """\
                    Webmap Generator

Objective
  Generate an interactive map of the world featuring 2 toggleable
  map overlays."""
_epilog = """\
Detail
  The script uses two datasets while generating the map. One
  dataset contains world population data. The other dataset
  details volcano sites around the world.

  - Population by Country (2005 data), assign a color code to
    each country determined by comparison with three population
    thresholds.

  - Volcanoes of the World (GVP data), place map markers at all
    sites around the world that show or have shown volcanic
    activity. GVP refers to the Global Volcanism Program."""
__doc__ = f"""\
{_description}
{_epilog}"""


def _load_from_config(path):
    """When available, load project-level configuration variables.

    :param path: str
    :return: str
    """
    try:
        sys.path.insert(0, os.path.abspath(path))
        import project
        return project.data_dir

    except ImportError:
        return '.'

    finally:
        sys.path = sys.path[1:]


def _generate_color_string(elevation):
    """Determine appropriate color-string based on elevation, and return it.

    :param elevation: str
    :return: str
    """
    """List of valid color strings for folium markers:
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

    :param name: str
    :param elev: str
    :param detail_url: str
    :param height: str
    :param width: str
    :param embed_url: str
    :param bbox: str
    :param layer_type: str
    :return: str
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
    height = '400'
    width = '600'
    layer_type = 'cyclemap'
    lat_diff = 0.088
    lon_diff = 0.160
    fgv = folium.FeatureGroup(name="Volcanoes of the World (via GVP)")

    for num, name, elev, lat, lon in zip(nums, names, elevs, lats, lons):
        lat = float(lat)
        lon = float(lon)
        fill_color = _generate_color_string(elevation=elev)
        tooltip = f'{name} ({elev}m)'

        bbox = f'{lon-lon_diff}%2C{lat-lat_diff}%2C{lon+lon_diff}%2C{lat+lat_diff}'
        detail_url = f'https://volcano.si.edu/volcano.cfm?vn={num}&vtab=GeneralInfo'
        popup = _generate_popup(name=name, elev=elev, detail_url=detail_url,
                                height=height, width=width, embed_url=embed_url,
                                bbox=bbox, layer_type=layer_type)

        fgv.add_child(child=folium.RegularPolygonMarker(
            location=[lat, lon], color='white', radius=10, weight=1,
            number_of_sides=3, rotation=30, fill_opacity=0.7,
            fill_color=fill_color, tooltip=tooltip, popup=popup))

    return fgv


def _parse_volcano_data(dataframe):
    """Parse columns of data from dataframe.

    Return selected column data as a tuple of lists.

    :param dataframe: pandas.DataFrame
    :return: tuple
    """
    numbers = list(dataframe["Volcano Number"])
    names = list(dataframe["Volcano Name"])
    elevations = list(dataframe["Elevation (m)"])
    latitudes = list(dataframe["Latitude"])
    longitudes = list(dataframe["Longitude"])

    return numbers, names, elevations, latitudes, longitudes


def _generate_population_layer(file):
    """Generate "Population by Country" FeatureGroup layer and return it.

    :param file: str
    :return: folium.FeatureGroup
    """
    fgp = folium.FeatureGroup(name="Population by Country (2005 data)")

    layer = folium.GeoJson(data=open(file, 'r', encoding='utf-8-sig').read(),
        style_function=lambda x: {'weight': 0, 'fillColor':
            'yellow' if x['properties']['POP2005'] < 10000000
            else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
            else 'red'}
    )

    fgp.add_child(child=layer)

    return fgp


def generate_webmap(data_dir):
    """Generate a folium.Map, add two FeatureGroup layers, and return it.

    :param data_dir: str
    :return: folium.Map
    """
    webmap = folium.Map(location=[38.000, -99.000], tiles="Mapbox Bright")
    population_layer = _generate_population_layer(file=f'{data_dir}/world.json')
    webmap.add_child(child=population_layer)
    dataframe = gvp.load_dataframe(data_dir=data_dir)
    nums, names, elevs, lats, lons = _parse_volcano_data(dataframe=dataframe)
    volcano_layer = _generate_volcano_layer(nums=nums, names=names, elevs=elevs,
                                            lats=lats, lons=lons)
    webmap.add_child(child=volcano_layer)
    webmap.add_child(child=folium.LayerControl())

    return webmap


def write_webmap(webmap, file):
    """Save instance of folium.Map as html file to local filesystem.

    :param webmap: folium.Map
    :param file: str
    :return: None
    """
    webmap.save(outfile=file)


def _parse_args():
    """Parse and validate command line arguments.

    Return the arguments with their values. Print the module's
    usage message when the arguments are determined to be invalid.

    :param args: None
    :return: types.SimpleNamespace
    """
    parser = ArgumentParser(description=_description, epilog=_epilog,
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('-d', '--data', type=str, default=data_dir,
                        help='Directory to use for local data assets.')
    parser.add_argument('-s', '--save', type=str, default=save_dir,
                        help='Directory to use to save the webmap file.')
    return parser.parse_args()


data_dir = _load_from_config(path=_path_to_config)
save_dir = '.'
save_file = 'webmap.html'

if __name__ == '__main__':
    args = _parse_args()
    data_dir = args.data
    save_dir = args.save

    webmap = generate_webmap(data_dir=data_dir)
    write_webmap(webmap=webmap, file=f'{save_dir}/{save_file}')

    print(f'Webmap page saved to file:\n  {save_dir}/{save_file}')
