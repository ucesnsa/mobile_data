import geopandas as gpd
from mpl_toolkits.basemap import Basemap as Basemap
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import shapefile
from matplotlib.lines import Line2D

SELECTED_ORIGIN_COUNT = 10

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)

# map data
file_shape_london = 'data/mygeodata_wgs84/greater_london_const_region'
file_geojson = 'data/geojson/greater_london.geojson'

# plot data
file_origin_sum = 'data/Origin_sum.csv'
file_od = 'data/OD(L1).csv'

df_json = gpd.read_file(file_geojson)
df_origin_sum = pd.read_csv(file_origin_sum)
df_od = pd.read_csv(file_od)

df_origin_sum = df_origin_sum.sort_values(by=['sum'], ascending=False)
df_origin_sum = df_origin_sum.iloc[:SELECTED_ORIGIN_COUNT]

df_json["lon"] = df_json["geometry"].centroid.x
df_json["lat"] = df_json["geometry"].centroid.y

# df_json.crs = 4326  # this line

df_json = df_json.to_crs(epsg=4326)

# find the OD for the selected origin codes
df_od_merged = df_origin_sum[['origin_code']].merge(df_od, left_on=['origin_code'],
                                                    right_on=['origin_code'], how='inner')
# print(df_od_merged.head(20))
# df_od_merged.to_csv('data/df_od_merged.csv')

df_od_merged = df_od_merged.rename(columns={'origin_code': 'source',
                                            'destination_code': 'target',
                                            'sum': 'weight'
                                            })
df_od_merged = df_od_merged.loc[df_od_merged['source'] != df_od_merged['target']]

graph = nx.from_pandas_edgelist(df_od_merged, edge_attr=True, create_using=nx.DiGraph())

plt.figure(figsize=(10, 9))

sf = shapefile.Reader(file_shape_london)

x0, y0, x1, y1 = sf.bbox
cx, cy = (x0 + x1) / 2, (y0 + y1) / 2

m = Basemap(llcrnrlon=x0, llcrnrlat=y0, urcrnrlon=x1, urcrnrlat=y1, lat_0=cx, lon_0=cy, resolution='c',
            projection='merc')
m.readshapefile(file_shape_london, 'metro', linewidth=.15)
mx, my = m(df_json['lon'].values, df_json['lat'].values)

pos = {}
for count, elem in enumerate(df_json['_index']):
    pos[elem] = (mx[count], my[count])

origin_node_list = df_origin_sum['origin_code'].tolist()
all_nodes_list = graph.nodes()

# find all non origin nodes
non_origin_node_list = [x for x in all_nodes_list if x not in origin_node_list]
# draw non-origin nodes
nx.draw_networkx_nodes(G=graph, pos=pos, nodelist=non_origin_node_list,  # nodelist=graph.nodes(),
                       node_color='#1E475C', alpha=0.8, node_size=30)
# draw origin nodes
nx.draw_networkx_nodes(G=graph, pos=pos, nodelist=origin_node_list,  # nodelist=graph.nodes(),
                       node_color='#de981f', alpha=0.8, node_size=30)

edges = graph.edges()
weights = [graph[u][v]['weight'] for u, v in edges]
MAX_WEIGHT = max(weights)
MAX_WIDTH = 3
weights2 = [(w / MAX_WEIGHT) * MAX_WIDTH for w in weights]
nx.draw_networkx_edges(G=graph, pos=pos, alpha=0.9, arrows=True,
                       edge_color='#6BB0D6', width=weights2
                       )

# Avoid border around map.
m.drawmapboundary(fill_color='#ffffff', linewidth=.0)
plt.tight_layout()

# add legend
legend_elements = [Line2D([0], [0], marker='o', color='w', label='Origin',
                          markerfacecolor='#de981f', markersize=10),
                   Line2D([0], [0], marker='o', color='w', label='Destination',
                          markerfacecolor='#1E475C', markersize=10)]

plt.legend(handles=legend_elements, loc='upper right')

plt.savefig("./images/map_1.png", format="png", dpi=300)
plt.show()
