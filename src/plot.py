# Importing libaries
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster
from src.criteria import conditions

# Defining icons styles

icons = ['Icon(color = "red", opacity = 0.1, prefix = "fa", icon = "times",icon_color = "black")', 
'Icon(color = "purple", opacity = 0.1, prefix = "fa", icon = "pencil-square", icon_color = "white")',
'Icon(color = "blue", opacity = 0.1, prefix = "fa", icon = "graduation-cap", icon_color = "black")',
'Icon(color = "red", opacity = 0.1, prefix = "fa", icon = "building", icon_color = "black")',
'Icon(color = "green", opacity = 0.1, prefix = "fa", icon = "coffee", icon_color = "white")',
'Icon(color = "black",opacity = 0.1, prefix = "fa", icon = "plane", icon_color = "white")',
'Icon(color = "lightgreen", opacity = 0.1, prefix = "fa",  icon = "glass", icon_color = "black")',
'Icon(color = "lightgray", opacity = 0.1, prefix = "fa", icon = "leaf", icon_color = "green")',
'Icon(color = "orange", opacity = 0.1, prefix = "fa", icon = "futbol-o", icon_color = "white")',
'Icon(color = "white", opacity = 0.1, prefix = "fa", icon = "paw", icon_color = "orange")'
]

def to_dic(df, row):
    '''
    Returns a row of a Dataframe in a dictonary format
    '''
    return df.iloc[[row]].to_dict(orient='records')[0]

def plot_map(dic, save=False):
    '''
    Function that pass a dictionary created from a row of the dataframe and plots all the locations in the map
    Parameters:
        dic: dic
            Dictionary created from a Dataframe row  ex: df.iloc[[0]].to_dict(orient='records')[0]
        save: bool (Default: False)
            Save the generated map into an html file
            
    '''
    m = Map(location=[dic["latitude"], dic["longitude"]], zoom_start=15)
    popup = f"This is the office of {dic['name']} that we want to take over"
    Marker(
                            [dic["latitude"], dic["longitude"]], 
                            popup=popup, 
                            tooltip="Location of the company",
                            icon=eval(icons[0])
                            ).add_to(m)
    
    for c in range(1,len(conditions)+1):
        if f"condition{c}_results" in dic and dic[f"condition{c}_results"]:
            for loc in dic[f"condition{c}_results"]:
                mark = {
                    "location":[loc["latitude"], loc["longitude"]],
                    "tooltip" : conditions[c]["tag"],
                    "popup": f"<b>{loc['name']}</b>"
                       }
                Marker(**mark, icon=eval(icons[c])).add_to(m)
    if save:
        m.save(f"./img/{dic['name']}.html")
    return m