from osmnx import *


def amenities_from_place(query, network_type='all_private', simplify=True, retain_all=False,
                     truncate_by_edge=False, name='unnamed', which_result=1, buffer_dist=None, timeout=180, memory=None, max_query_area_size=50*1000*50*1000, clean_periphery=True):

    # create a GeoDataFrame with the spatial boundaries of the place(s)
    if isinstance(query, str) or isinstance(query, dict):
        # if it is a string (place name) or dict (structured place query), then it is a single place
        gdf_place = core.gdf_from_place(query, which_result=which_result, buffer_dist=buffer_dist)
        name = query
    elif isinstance(query, list):
        # if it is a list, it contains multiple places to get
        gdf_place = core.gdf_from_places(query, buffer_dist=buffer_dist)
    else:
        raise ValueError('query must be a string or a list of query strings')

    # extract the geometry from the GeoDataFrame to use in API query
    polygon = gdf_place['geometry'].unary_union
    log('Constructed place geometry polygon(s) to query API')

    # download amenities within geometry.
    G = amenities_from_polygon(polygon, network_type=network_type)
    return G

print(amenities_from_place('Chicago, Illinois', network_type='station'))
