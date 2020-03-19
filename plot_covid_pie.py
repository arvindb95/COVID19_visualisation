import geopandas
import pandas
import matplotlib.pyplot as plt

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

world.plot(color="white",edgecolor="black")
for centroid_id in range(len(world.centroid)):
    centroid = world.centroid[centroid_id]
    lat,lon = centroid.x, centroid.y
    plt.plot(lat,lon,"ko")
plt.show()
