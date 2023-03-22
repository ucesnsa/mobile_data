import geopandas as gpd
from mpl_toolkits.basemap import Basemap as Basemap
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import shapefile
from matplotlib.lines import Line2D
from mylib import db_utils as dl

NON_CLUSTER_NODE_COLOUR = '#86a4bd'
NON_CLUSTER_NODE_WT = 20
CLUSTER_NODE_WT = 30


def get_colour_list(lst):
    c_red = 210
    c_green = 20
    c_blue = 20
    increment = 20
    col_lst = list()
    for i, item in enumerate(lst):
        c_red = c_red - int(increment / 10)
        # c_blue = c_blue + increment
        c_green = c_green + increment
        base_value = "%x%x%x" % (c_red, c_green, c_blue)
        col_lst.append((item, '#' + base_value))
    return col_lst


def add_legend(pl, src_cl_lst, node_loc):
    handle_lst = list()
    index = 0
    for hex_id, hex_colour in src_cl_lst:
        l1 = Line2D([0], [0], marker='o', color='w', label=hex_id,
                    markerfacecolor=hex_colour, markersize=4)
        print(hex_id, ' - ', node_loc[index])
        index = index + 1
        handle_lst.append(l1)

    # legend_elements = np.array(handle_lst)
    pl.legend(handles=handle_lst, loc='best')


def create_od_cluster_plot(df_od_merged, df_json, direction_type, title, root_loc):
    base_location = root_loc

    # map data
    file_shape_london = base_location + 'data/mygeodata_wgs84/greater_london_const_region'

    output_image_file = base_location + 'images/cluster_map {0}.png'.format(title)
    img_title = title


    graph = nx.from_pandas_edgelist(df_od_merged, edge_attr=True, create_using=nx.DiGraph())

    plt.figure(figsize=(10, 10))

    sf = shapefile.Reader(file_shape_london)

    x0, y0, x1, y1 = sf.bbox
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2

    m = Basemap(llcrnrlon=x0, llcrnrlat=y0, urcrnrlon=x1, urcrnrlat=y1,
                lat_0=cx, lon_0=cy, resolution='c', projection='merc')

    m.readshapefile(file_shape_london, 'metro', linewidth=.15)
    mx, my = m(df_json['lon'].values, df_json['lat'].values)
    x_loc, y_loc = (df_json['lon'].values, df_json['lat'].values)

    pos = {}
    pos_org = {}
    for count, elem in enumerate(df_json['_index']):
        pos[elem] = (mx[count], my[count])
        pos_org[elem] = (y_loc[count], x_loc[count]) # change to lat, lon

    all_nodes_list = graph.nodes()
    edges = graph.edges()
    weights = [graph[u][v]['weight'] for u, v in edges]

    if direction_type == 'SOURCE':
        cluster_node_list = df_od_merged['source'].unique().tolist()
        cluster_colour_list = get_colour_list(cluster_node_list)
        cluster_node_loc = [pos_org[n] for n in cluster_node_list]

        # loop through two list with tuples of two values
        edge_colours = [t[1] for t in cluster_colour_list for s in edges if t[0] == s[0]]
    else:
        cluster_node_list = df_od_merged['target'].unique().tolist()
        cluster_colour_list = get_colour_list(cluster_node_list)
        cluster_node_loc = [pos_org[n] for n in cluster_node_list]

        # loop through two list with tuples of two values
        edge_colours = [t[1] for t in cluster_colour_list for s in edges if t[0] == s[1]]


    # find all non origin nodes
    non_cluster_node_list = [x for x in all_nodes_list if x not in cluster_node_list]

    # draw non-cluster nodes
    nx.draw_networkx_nodes(G=graph, pos=pos, nodelist=non_cluster_node_list,  # nodelist=graph.nodes(),
                           node_color=NON_CLUSTER_NODE_COLOUR, alpha=0.01, node_size=NON_CLUSTER_NODE_WT)

    # draw cluster nodes
    nx.draw_networkx_nodes(G=graph, pos=pos, nodelist=cluster_node_list,  # nodelist=graph.nodes(),
                           node_color=[t[1] for t in cluster_colour_list],
                           alpha=0.9, node_size=CLUSTER_NODE_WT)

    max_wt = max(weights)
    max_width = 4
    weights2 = [round((w / max_wt) * max_width, 2) for w in weights]
    nx.draw_networkx_edges(G=graph, pos=pos, alpha=0.6, arrows=True,
                           edge_color=edge_colours, width=weights2)

    add_legend(plt, cluster_colour_list, cluster_node_loc)

    # Avoid border around map.
    m.drawmapboundary(fill_color='#ffffff', linewidth=.0)
    plt.title(img_title)
    plt.tight_layout()

    plt.savefig(output_image_file, format="png", dpi=300)
    #plt.show()



# run it
#file_system_root = '../'
#create_od_cluster_plot(file_system_root)
