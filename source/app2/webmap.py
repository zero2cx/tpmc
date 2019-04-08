import folium
import gvp_volcanoes as gvp

__doc__ = """\
"""
_repo = 'https://hithib.com/zero2cx/tpmc'
_author = 'David Schenck, aka zero2cx'
_version = '0.9.3'
_disclaimer = """\
Adapted from the Application 2 exercise:
The Python Mega Course, <https://www.udemy.com/the-python-mega-course>
Course creator, Ardit Sulce <https://www.udemy.com/user/adiune>"""


"""List of valid Marker colors:
red, darkred, lightred, orange, beige, green, darkgreen, lightgreen,
blue, darkblue, lightblue, cadetblue, purple, darkpurple, pink,
white, gray, lightgray, black"""
def _generate_color_string(elevation):
    """Determine the appropriate color-string based on elevation and return it.

    :param elevation:
    :return:
    """
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


def _generate_volcano_layer(nums, names, elevs, lats, lons):
    """Generate the "Volcanoes of the World" FeatureGroup and return it.

    :param names:
    :param elevs:
    :param lats:
    :param lons:
    :return:
    """
    embed_url = 'https://www.openstreetmap.org/export/embed.html'
    height = 200
    width = 400
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
        caption = f"""\
            <strong style="float: left;">{name} ({elev}m)</strong>
            <em style="float: right;"><a href="{detail_url}" target="_blank" 
              rel="noopener noreferrer">Site detail</a></em><br/>"""
        popup = f"""\
            <iframe frameborder="0" scrolling="no" style="border: 1px solid black"
              height="{height}" width="{width}" marginheight="0" marginwidth="0"
              src="{embed_url}?bbox={bbox}&amp;layer={layer_type}"></iframe><br/>
            {caption}"""

        fgv.add_child(folium.RegularPolygonMarker(
            location=[lat, lon], color='white', radius=10, weight=1,
            number_of_sides=3, rotation=30, fill_opacity=0.7,
            fill_color=fill_color, tooltip=tooltip, popup=popup))

    return fgv


def _parse_volcano_data(data):
    """

    :param data:
    :return:
    """
    numbers = list(data["Volcano Number"])
    names = list(data["Volcano Name"])
    elevations = list(data["Elevation (m)"])
    latitudes = list(data["Latitude"])
    longitudes = list(data["Longitude"])

    return numbers, names, elevations, latitudes, longitudes


def _generate_population_layer(filename):
    """Generate the "Population by Country" FeatureGroup and return it.

    :return:
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


def generate_map():
    map = folium.Map(location=[38.000, -99.000], tiles="Mapbox Bright")
    population_layer = _generate_population_layer('../../assets/data/world.json')
    map.add_child(population_layer)
    dataframe = gvp.load_dataframe()
    nums, names, elevs, lats, lons = _parse_volcano_data(dataframe)
    volcano_layer = _generate_volcano_layer(nums, names, elevs, lats, lons)
    map.add_child(volcano_layer)
    map.add_child(folium.LayerControl())

    return map

def save_map(map):
    """

    :param map:
    :return:
    """
    map.save(filename)


if __name__ == '__main__':
    import os
    path = '/'.join(os.getcwd().split('\\'))
    filename = 'webmap.html'
    map = generate_map()
    save_map(map)
    print(f'Webmap page saved to file:\n  file:///{path}/{filename}')
