import geopandas as gpd
import numpy as np
import matplotlib.pyplot
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

from scipy.stats import norm
#import geoplot.crs as gcrs

#data = (3,6,7,8,16)

#fig, simplechart = matplotlib.pyplot.subplots()
#simplechart.plot(data)
#matplotlib.pyplot.show()
#exit(-1)

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)

# read files
read_csv = 'OD(L1).csv'
read_json = 'greater_london.geojson'

#read in dataframe
df_OD = pd.read_csv(read_csv)
#df_json = pd.read_json(read_json)

#basic statisitc
df_OD.describe()
print(df_OD.describe())
df_OD['sum_norm'] = np.log(df_OD['sum'])
df_OD = sn.displot(df_OD, x="sum_norm", bins=20, stat="probability")

#figure = df_OD.get_figure()
#figure.savefig('Probability_Distribution.png', dpi=300)
# displaying the title
#plt.title("Probability Distribution")

#plt.title("Destination_sum")
#df_new.plot(column='sum')

#save fig png
plt.savefig('Probability Distribution.png', dpi=300)
matplotlib.pyplot.show()

#Task6. Once we decide which Hex to look at, we need a map of the actual flows.

#Ideally, we need to take a network approach where each Hex is a node, and the links and weights come from
#the OD matrix. But for a quick look, we can do the following:
#Rank all Origin from higher to low sum_numer_of_users. We will have a fat tail of small ranks, as expected.
#Let's make an arbitrary cut of the first 50 ranks and then find all the Destination Hex for these 100. We can produce a couple of maps:
#Plot the 50Hex along with their corresponding Destination Hexagons.
#Plot the actual flows between polygons. There are some packages in Python or plug-ins in QGIS to draw flows
#between points. I don't remember the right now names but you can google around.