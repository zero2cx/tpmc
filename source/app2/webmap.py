import folium
from source.app2 import gvp_volcanoes as gvp

_repo = 'https://hithib.com/zero2cx/tpmc'
_author = 'David Schenck, aka zero2cx'
_version = '0.9.2'
_disclaimer = """\
Adapted from the Application 2 exercise:
The Python Mega Course, <https://www.udemy.com/the-python-mega-course>
Course creator, Ardit Sulce <https://www.udemy.com/user/adiune>"""


# TODO inspect folium.Marker source to validate each of the following colors
"""red, blue, gray, darkred, lightred, orange, beige, green,
darkgreen, lightgreen, darkblue, lightblue, purple,
darkpurple, pink, cadetblue, lightgray, black, white"""
def generate_color(elevation):
    """Determine the color-string based on elevation and return it.

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


def generate_volcano_layer(names, elevs, lats, lons):
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
    fgv = folium.FeatureGroup(name="Volcanoes of the World")

    for name, elev, lat, lon in zip(names, elevs, lats, lons):

        lat = float(lat)
        lon = float(lon)

        bbox = f'{lon-lon_diff}%2C{lat-lat_diff}%2C{lon+lon_diff}%2C{lat+lat_diff}'

        popup = f"""\
            <iframe frameborder="0" scrolling="no" style="border: 1px solid black"
            height="{height}" width="{width}" marginheight="0" marginwidth="0"
            src="{embed_url}?bbox={bbox}&amp;layer={layer_type}"></iframe><br/>
            <strong>{name} ({elev}m)</strong>           <em>View image</em>
            """

        tooltip = f'{name} ({elev}m)'

        fgv.add_child(folium.RegularPolygonMarker(
            location=[lat, lon], color='white', radius=10, weight=1,
            number_of_sides=3, rotation=30, fill_opacity=0.7,
            fill_color=generate_color(elev),
            popup=popup, tooltip=tooltip))

    return fgv


def parse_volcano_data(data):
    """

    :param data:
    :return:
    """
    names = list(data["Volcano Name"])
    elevations = list(data["Elevation (m)"])
    latitudes = list(data["Latitude"])
    longitudes = list(data["Longitude"])

    return names, elevations, latitudes, longitudes


def generate_population_layer(filename):
    """Generate the "Population by Country" FeatureGroup and return it.

    :return:
    """
    fgp = folium.FeatureGroup(name="Population by Country (2005 data)")

    fgp.add_child(folium.GeoJson(
        data=open(filename, 'r', encoding='utf-8-sig').read(),
        style_function=lambda x: {'fillColor':
            'yellow' if x['properties']['POP2005'] < 10000000
            else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
            else 'red'
        }))

    return fgp


if __name__ == '__main__':
    map = folium.Map(
        location=[38.000, -99.000], zoom_start=6, tiles="Mapbox Bright")
    map.add_child(generate_population_layer('../../assets/data/world.json'))
    data = gvp.load_dataframe()
    names, elevs, lats, lons = parse_volcano_data(data)
    map.add_child(generate_volcano_layer(names, elevs, lats, lons))
    map.add_child(folium.LayerControl())
    map_title = "TPMC App2 - Map"
    map.save(f'{map_title}.html')
    print(f'Webmap page saved to file: {map_title}.html')
