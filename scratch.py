import geopandas as gpd
from mpl_toolkits.basemap import Basemap as Basemap
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from descartes import PolygonPatch
import matplotlib
from matplotlib.collections import PatchCollection
import contextily as cx
import folium
from os import environ
import matplotlib.pyplot as plt
import shapefile

SELECTED_ORIGIN_COUNT = 10

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)

file_geojson = 'data/greater_london.geojson'
file_origin_sum = 'data/Origin_sum.csv'
file_od = 'data/OD(L1).csv'
file_shape_london = 'data/mygeodata_wgs84/greater_london_const_region'


df_json = gpd.read_file(file_geojson)
df_origin_sum = pd.read_csv(file_origin_sum)
df_od = pd.read_csv(file_od)


df_origin_sum = df_origin_sum.sort_values(by=['sum'], ascending=False)
df_origin_sum = df_origin_sum.iloc[:SELECTED_ORIGIN_COUNT]

df_json["lon"] = df_json["geometry"].centroid.x
df_json["lat"] = df_json["geometry"].centroid.y

# find the OD for the selected origin codes
df_od_merged = df_origin_sum[['origin_code']].merge(df_od, left_on=['origin_code'],
                                                    right_on=['origin_code'], how='inner')

df_od_merged = df_od_merged.rename(columns={'origin_code': 'source',
                                            'destination_code': 'target',
                                            'sum': 'weight'
                                            })

graph = nx.from_pandas_edgelist(df_od_merged, edge_attr=True)

df_json.crs = 4326  # this line
map_df = df_json.to_crs(epsg=3857)

plt.figure(figsize=(10, 9))

sf = shapefile.Reader(file_shape_london)

x0, y0 ,x1, y1 = sf.bbox
cx, cy = (x0 + x1) / 2, (y0 + y1) / 2

m = Basemap(llcrnrlon=x0, llcrnrlat=y0, urcrnrlon=x1, urcrnrlat=y1, lat_0=cx, lon_0=cy, resolution='c', projection='mill')
m.readshapefile(file_shape_london, 'metro', linewidth=.15)
mx, my = m(df_json['lon'].values, df_json['lat'].values)

pos = {}
for count, elem in enumerate(df_json['_index']):
    pos[elem] = (mx[count], my[count])

nx.draw_networkx_nodes(G=graph, pos=pos, nodelist=graph.nodes(),
                       node_color='r', alpha=0.8, node_size=1)
nx.draw_networkx_edges(G=graph, pos=pos, edge_color='g',
                       alpha=0.8, arrows=True, width=1)

# Avoid border around map.
m.drawmapboundary(fill_color='#ffffff', linewidth=.0)
plt.tight_layout()
plt.savefig("./images/map_1.png", format="png", dpi=300)
plt.show()
