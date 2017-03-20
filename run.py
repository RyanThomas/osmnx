from osmnx import *
from compactness.calc import *
import json

name = "Tallinn, Estonia"
stations = amenities_from_place(name, network_type='station')[0]
amenities = amenities_from_place(name, network_type='amenity')[0]

scores = calc_compactness(amenities['elements'], stations['elements'])

x = to_geojson(scores)
json.dump(x, open('test.json', 'w'), indent=2)
