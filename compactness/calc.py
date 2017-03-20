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

# Both must be dictionaries containing lat, and lng.
# Score and name are optional, other keys will be preserved.
def calc_compactness(lower_scale_nodes, centers, radius=1000, save=False):
    all_scores = [0 for i in range(len(centers))]
    for i in range(len(centers)):
        for node in lower_scale_nodes:
            dist = vincenty((centers[i]['lat'], centers[i]['lon']), (node['lat'], node['lon'])).meters
            if dist <= radius:
                if 'score' in node.keys():
                    score = node['score'] * get_density(node['lat'],node['lon']) / ((dist)**2)
                else:
                    score = get_density(node['lat'],node['lon']) / ((dist)**2)

                all_scores[i] += score

    for i in range(len(centers)):
        centers[i]['score'] = all_scores[i]

    return centers
