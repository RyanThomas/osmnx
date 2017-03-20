from geopy.distance import vincenty

def get_density(lat, lon):
    return 1

def to_geojson(osm_elements):
    features = []
    for i in osm_elements:
        i['geometry'] = {}
        i['geometry']['type'] = 'Point'
        i['geometry']['coordinates'] = [i['lon'], i['lat']]
        i['properties'] = {}
        for key, value in i.items():
            if key != 'geometry' and key != 'properties':
                i['properties'][key] = value
        i = {'properties': i['properties'], 'geometry': i['geometry'], 'type': 'Feature'}
        features.append(i)
    return {'type': 'FeatureCollection', 'features': features}

def distance_to_nearest_center(lat,lon,stations, neighborhood_radius):
    m = -100000000
    d = vincenty((lat,lon),(lat,lon))
    for i in stations:
        lat1 = i['lat']
        lon1 = i['lon']
        if lat!=lat1 and lon!=lon1 and vincenty((lat,lon),(lat1,lon1)).meters <= neighborhood_radius:
            if float(i['score']) >= m:
                m = float(i['score'])
                d = vincenty((lat,lon),(lat1,lon1))
    return d.meters

# Both must be dictionaries containing lat, and lng.
# Score and name are optional, other keys will be preserved.
def calc_compactness(amenities, stations, station_radius=1000, neighborhood_radius=10000, save=False):
    all_scores = [0 for i in range(len(stations))]
    for i in range(len(stations)):
        for node in amenities:
            dist = vincenty((stations[i]['lat'], stations[i]['lon']), (node['lat'], node['lon'])).meters
            if dist <= station_radius and dist != 0:
                if 'score' in node.keys():
                    score = node['score'] * get_density(node['lat'],node['lon']) / ((dist/1000)**2)
                else:
                    score = get_density(node['lat'],node['lon']) / ((dist/1000)**2)

                all_scores[i] += score

    for i in range(len(stations)):
        stations[i]['score'] = all_scores[i]

    for i in range(len(stations)):
        s = stations[i]
        d = distance_to_nearest_center(s['lat'], s['lon'], stations, neighborhood_radius)
        if d != 0:
            stations[i]['score'] = stations[i]['score'] / ((d/1000)**2)

    return stations
