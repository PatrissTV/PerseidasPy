# Import gmplot library.
from gmplot import *
# Place map
# First two arugments are the geogrphical coordinates .i.e. Latitude and Longitude
#and the zoom resolution.
gmap=gmplot.GoogleMapPlotter(17.438139, 78.39583, 10)

# Because google maps is not a free service now, you need to get an api key. Else commenting
# below line you will see the maps with "For Development Purpose Only" on the screen and maps
# with low resolution.
#gmap.apikey = "Your_API_KEY"
gmap.apikey = "AIzaSyDeRNMnZ__VnQDiATiuz4kPjF_c9r1kWe8"
# Location where you want to save your file.


def plot(lat,lng):
    gmap.plot(lat, lng, 'cornflowerblue', edge_width = 3.0)


def pos(lat,lng):
    gmap.scatter(lat, lng, 'k', marker=True)

def draw():
    gmap.draw( "map.html" )
