import geopandas as gpd
from mpl_toolkits.basemap import Basemap as Basemap
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import shapefile
from matplotlib.lines import Line2D

NON_CLUSTER_NODE_COLOUR = '#99ccff'
CLUSTER_NODE_COLOUR = '#ff9999'
NON_CLUSTER_NODE_WT = 20
CLUSTER_NODE_WT = 30
CLUSTER_NODE_ALPHA = 0.9
NON_CLUSTER_NODE_ALPHA = 0.1


def create_network_plot(df_od_merged, df_json, direction_type, title, root_loc):
    base_location = root_loc
    # map data
    file_shape_london = base_location + 'data/mygeodata_wgs84/greater_london_const_region'

    # plot data
    output_image_file = base_location + 'images/network_map {0}.png'.format(title)
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

    pos = {}
    for count, elem in enumerate(df_json['_index']):
        pos[elem] = (mx[count], my[count])

    target_node_list = df_od_merged['target'].unique().tolist()
    all_nodes_list = graph.nodes()

    # find all non origin nodes
    non_target_node_list = [x for x in all_nodes_list if x not in target_node_list]

    if direction_type == 'SOURCE':
        cluster_nodes = non_target_node_list
        non_cluster_nodes = target_node_list
        source_colour = CLUSTER_NODE_COLOUR
        dest_colour = NON_CLUSTER_NODE_COLOUR
        source_alpha = CLUSTER_NODE_ALPHA
        dest_alpha = NON_CLUSTER_NODE_ALPHA
    else:
        cluster_nodes = target_node_list
        non_cluster_nodes = non_target_node_list
        source_colour = NON_CLUSTER_NODE_COLOUR
        dest_colour = CLUSTER_NODE_COLOUR
        source_alpha = NON_CLUSTER_NODE_ALPHA
        dest_alpha = CLUSTER_NODE_ALPHA

    # draw cluster nodes
    nx.draw_networkx_nodes(G=graph, pos=pos, nodelist=non_cluster_nodes,
                           node_color=NON_CLUSTER_NODE_COLOUR, alpha=NON_CLUSTER_NODE_ALPHA,
                           node_size=NON_CLUSTER_NODE_WT)
    # draw non_cluster nodes
    nx.draw_networkx_nodes(G=graph, pos=pos, nodelist=cluster_nodes,
                           node_color=CLUSTER_NODE_COLOUR, alpha=CLUSTER_NODE_ALPHA,
                           node_size=CLUSTER_NODE_WT)

    edges = graph.edges()
    weights = [graph[u][v]['weight'] for u, v in edges]
    max_wt = max(weights)
    max_width = 3
    weights2 = [(w / max_wt) * max_width for w in weights]

    nx.draw_networkx_edges(G=graph, pos=pos, alpha=0.4, arrows=True,
                           edge_color='#ad1c5d', width=weights2)

    # Avoid border around map.
    m.drawmapboundary(fill_color='#ffffff', linewidth=.0)
    plt.tight_layout()

    # add legend
    legend_elements = [Line2D([0], [0], marker='o', color='w', label='Origin',
                              markerfacecolor=source_colour, alpha=source_alpha),
                       Line2D([0], [0], marker='o', color='w', label='Destination',
                              markerfacecolor=dest_colour, alpha=dest_alpha)]

    plt.legend(handles=legend_elements, loc='best')
    plt.title(img_title)
    plt.tight_layout()
    plt.savefig(output_image_file, format="png", dpi=300)
    #plt.show()


# run it
#file_system_root = '../'
#create_network_plot(file_system_root)
