from osmnx import *
from compactness.calc import *
import json

def run(name):
    stations = amenities_from_place(name, network_type='station')[0]
    amenities = amenities_from_place(name, network_type='amenity')[0]

    scores = calc_compactness(amenities['elements'], stations['elements'])

    x = to_geojson(scores)
    json.dump(x, open(name + '.geojson', 'w'), indent=2)

run("Tallinn, Estonia")
run("Paris, France")
run("Seattle, Washington")
# run("London")
