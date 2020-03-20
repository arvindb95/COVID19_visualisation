import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.transforms as transforms
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

# Get latest data from worldometers.info
url = 'https://www.worldometers.info/coronavirus/#countries'
page_content = requests.get(url).text
soup = BeautifulSoup(page_content,'lxml')

table = soup.find("table",attrs={"id":"main_table_countries_today"})
table_data = table.tbody.find_all("tr")

# prob1 = total deaths
# prob2 = serious cases 
# prob3 = mild cases
# prob4 = recovered cases

country_names = []
total_cases = []
prob1s = []
prob2s = []
prob3s = []
prob4s = []

for country_number in range(len(table_data)):

    # Country name
    country_data = table_data[country_number].find_all("td")
    try:
        country_name = country_data[0].find("a").text
    except:
        country_name = country_data[0].text
    
    if (country_name == 'USA'):
        country_name = 'United States of America'
    if (country_name == 'S. Korea'):
        country_name = 'South Korea'
    if (country_name == 'UK'):
        country_name = 'United Kingdom'
    if (country_name == 'UAE'):
        country_name = 'United Arab Emirates'
    if (country_name == 'Eswatini'):
        country_name = 'eSwatini'
    if (country_name == 'Dominican Republic'):
        country_name = 'Dominican Rep.'
    if (country_name == 'North Macedonia'):
        country_name = 'Macedonia'
    if (country_name == 'Bosnia and Herzegovina'):
        country_name = 'Bosnia and Herz.'
    if (country_name == 'Brunei '):
        country_name = 'Brunei'
    if (country_name == 'DRC'):
        country_name = 'Dem. Rep. Congo'
    if (country_name == 'Ivory Coast'):
        country_name = "Côte d'Ivoire"
    if (country_name == 'Equatorial Guinea'):
        country_name = 'Eq. Guinea'
            
    country_names.append(country_name)

    # Country total cases
    country_total_cases = ''
    total_cases_list = table_data[country_number].find_all("td")[1].text.split(",")
    for i in range(len(total_cases_list)):
        country_total_cases = country_total_cases + total_cases_list[i]
    country_total_cases = int(country_total_cases)
    total_cases.append(country_total_cases)

    # Country total deaths 
    country_total_deaths = ''
    total_deaths_list = table_data[country_number].find_all("td")[3].text.split(",")    
    for i in range(len(total_deaths_list)):
        split_list = total_deaths_list[i].split(' ')
        final_str = ''
        for j in range(len(split_list)):
            final_str = final_str + split_list[j]
        total_deaths_list[i] = final_str
        country_total_deaths = country_total_deaths + total_deaths_list[i]
    if (country_total_deaths == ''):
        country_total_deaths = '0'
    country_total_deaths = int(country_total_deaths)
    prob1s.append(float(country_total_deaths/country_total_cases))

    # Country total serious
    country_total_serious = ''
    total_serious_list = table_data[country_number].find_all("td")[7].text.split(",")
    for i in range(len(total_serious_list)):
        country_total_serious = country_total_serious + total_serious_list[i]
    if (country_total_serious == ''):
        country_total_serious = '0'
    country_total_serious = int(country_total_serious)
    prob2s.append(float(country_total_serious/country_total_cases))

    # Country total mild
    country_total_active = ''
    total_active_list = table_data[country_number].find_all("td")[6].text.split(",")
    for i in range(len(total_active_list)):
        country_total_active = country_total_active + total_active_list[i]
    if (country_total_active == ''):
        country_total_active = '0'
    country_total_active = int(country_total_active)
    prob3s.append(float((country_total_active-country_total_serious)/country_total_cases))
    
    # Country total recovered 
    country_total_recovered = ''
    total_recovered_list = table_data[country_number].find_all("td")[5].text.split(",")
    for i in range(len(total_recovered_list)):
        country_total_recovered = country_total_recovered + total_recovered_list[i]
    if (country_total_recovered == ''):
        country_total_recovered = '0'
    country_total_recovered = int(country_total_recovered)
    prob4s.append(float(country_total_recovered/country_total_cases))    
    
############################################################################################################
# This is the required data

country_names = np.array(country_names)
total_cases = np.array(total_cases)
prob1s = np.array(prob1s)
prob2s = np.array(prob2s)
prob3s = np.array(prob3s)
prob4s = np.array(prob4s)
print(np.sort(country_names))
print(len(country_names))

#############################################################################################################

# Function to plot wedges

def draw_wedge(ax, drawing_origin, radius, prob1, prob2, prob3, prob4, col_alpha):

    box_height = 1
    box_width = 1
    
    origin = np.array([0,0])
    trans = (fig.dpi_scale_trans + transforms.ScaledTranslation(drawing_origin[0],drawing_origin[1], ax.transData))

    ang1 = prob1*360
    ang2 = prob2*360
    ang3 = prob3*360
    ang4 = prob4*360

    if (prob1 != 0):
        wedge1 = mpatches.Wedge(origin, radius, 0, ang1, facecolor="k", edgecolor="k", transform=trans, alpha=1)
        ax.add_patch(wedge1)
    if (prob2 != 0):
        wedge2 = mpatches.Wedge(origin, radius,ang1,ang1+ang2, facecolor="r", edgecolor="k", transform=trans, alpha=col_alpha)
        ax.add_patch(wedge2)
    if (prob3 != 0):
        wedge3 = mpatches.Wedge(origin, radius,ang1+ang2,ang1+ang2+ang3, facecolor="b", edgecolor="k", transform=trans, alpha=col_alpha)
        ax.add_patch(wedge3)
    if (prob4 != 0):    
        wedge4 = mpatches.Wedge(origin, radius,ang1+ang2+ang3,ang1+ang2+ang3+ang4, facecolor="y", edgecolor="k", transform=trans, alpha=col_alpha)
        ax.add_patch(wedge4)

    return 0

##### Plot world #####

fig = plt.figure(figsize=(16,8))
ax = fig.add_subplot(111)
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
world.plot(ax=ax, color="green",alpha=0.5,edgecolor="darkgreen",linewidth=0.5)
world_country_names = world['name'].values
country_lat, country_lon = world.centroid.x.values, world.centroid.y.values

scale = 1/max(total_cases)

print(np.sort(world_country_names))
print(len(world_country_names))

for country_num in range(len(country_names)):
    try:
        world_country_num = np.where(world_country_names == country_names[country_num])[0][0]
        do = (country_lat[world_country_num],country_lon[world_country_num])
        draw_wedge(ax,do,scale*total_cases[country_num],prob1s[country_num],prob2s[country_num],prob3s[country_num],prob4s[country_num],0.6)
    except:
        print(country_names[country_num]+" not found in world_country_names. Make sure that the naming conventions are the same in the two lists!")

legend_elements = [Line2D([],[], marker="o", color="k",linestyle="None", label="Deaths"), Line2D([0],[0], marker="o", color="r",linestyle="None", label="Severe cases"), Line2D([0],[0], marker="o", color="b",linestyle="None", label="Mild"), Line2D([0],[0], marker="o", color="y",linestyle="None", label="Recovered")]

ax.legend(handles=legend_elements, loc="center left")
plt.title("Most recent pie map of COVID19 cases around the world")
ax.text(-150,-75,"Data from : "+url)
plt.savefig("COVID19_pie_map.pdf")

