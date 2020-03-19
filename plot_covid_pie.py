import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
# Get latest data from worldometers.info
url = 'https://www.worldometers.info/coronavirus/#countries'
page_content = requests.get(url).text
soup = BeautifulSoup(page_content,'lxml')

table = soup.find("table",attrs={"id":"main_table_countries_today"})
table_data = table.tbody.find_all("tr")

country_names = []
for country_number in range(len(table_data)):
    country_data = table_data[country_number].find_all("td")
    try:
        country_name = country_data[0].find("a").text
        country_names.append(country_name)
    except:
        country_name = country_data[0].text
        country_names.append(country_name)

print(country_names)

# prob1 = total deaths
# prob2 = serious cases 
# prob3 = mild cases
# prob4 = recovered cases

def draw_wedge(ax, drawing_origin, radius, prob1, prob2, prob3, prob4, col_alpha):

    box_height = 1
    box_width = 1
    
    origin = np.array([0,0])
    trans = (fig.dpi_scale_trans + transforms.ScaledTranslation(drawing_origin[0],drawing_origin[1], ax.transData))

    ang1 = prob1*360
    ang2 = prob2*360
    ang3 = prob3*360
    ang4 = prob4*360
    ang5 = prob5*360

    if (prob1 != 0):
        wedge1 = mpatches.Wedge(origin, radius, 0, ang1, facecolor="y", edgecolor=None, transform=trans, alpha=col_alpha)
        ax.add_patch(wedge1)
    if (prob2 != 0):
        wedge2 = mpatches.Wedge(origin, radius,ang1,ang1+ang2, facecolor="b", edgecolor=None, transform=trans, alpha=col_alpha)
        ax.add_patch(wedge2)
    if (prob3 != 0):
        wedge3 = mpatches.Wedge(origin, radius,ang1+ang2,ang1+ang2+ang3, facecolor="g", edgecolor=None, transform=trans, alpha=col_alpha)
        ax.add_patch(wedge3)
    if (prob4 != 0):    
        wedge4 = mpatches.Wedge(origin, radius,ang1+ang2+ang3,ang1+ang2+ang3+ang4, facecolor="purple", edgecolor=None, transform=trans, alpha=col_alpha)
        ax.add_patch(wedge4)

    return 0
##### Plot world #####
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
world.plot(color="green",alpha=0.5,edgecolor="black",linewidth=0.5,figsize=(16,9))
country_name = world['name']
country_lat, country_lon = world.centroid.x, world.centroid.y

point_country_names = []

for centroid_id in range(len(world.centroid)):
    lat, lon = country_lat[centroid_id], country_lon[centroid_id]
    plt.plot(lat,lon,"ko")
    point_country_names.append(world['name'][centroid_id])
print(point_country_names)
#plt.show()
