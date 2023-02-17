import pandas
from mylib import od_cluster_map as cl
from mylib import od_network_plot as nt
from mylib import db_utils as dl
from pandas import DataFrame
import geopandas as gpd


def get_basemap_data(base_location) -> gpd.geodataframe:
    file_geojson = base_location + 'data/geojson/greater_london.geojson'
    df_g = gpd.read_file(file_geojson)
    df_g["lon"] = df_g["geometry"].centroid.x
    df_g["lat"] = df_g["geometry"].centroid.y
    df_g = df_g.to_crs(epsg=4326)
    return df_g


def run_all(data_source, data_level, direction_type):
    # run it
    file_system_root = ''

    obj_util = dl.DataManager()

    # get data
    # data source can be {worker, all}
    # data level can {l1, l2}
    file_name = 'sql/{0}_od_top10dest_{1}.sql'.format(data_source, data_level)

    df_od_merged = obj_util.get_od(file_name)

    # get data
    df_json = get_basemap_data(file_system_root)

    # create plots
    img_title = 'Top 10 destinations({0}, {1})'.format(data_source, data_level)

    # cluster plot
    cl.create_od_cluster_plot(df_od_merged, df_json, direction_type, img_title, file_system_root)

    # network plot
    nt.create_network_plot(df_od_merged, df_json, direction_type, img_title, file_system_root)


# data source can be {worker, all}
# data level can {l1, l2}
# set direction_type as TARGET for top n destination and SOURCE for origin

direction = 'TARGET'
data_src = 'worker'
data_lvl = 'l1'
run_all(data_src, data_lvl, direction)
direction = 'SOURCE'
data_lvl = 'l2'
run_all(data_src, data_lvl, direction)

direction = 'TARGET'
data_src = 'all'
data_lvl = 'l1'
run_all(data_src, data_lvl, direction)
direction = 'SOURCE'
data_lvl = 'l2'
run_all(data_src, data_lvl, direction)
