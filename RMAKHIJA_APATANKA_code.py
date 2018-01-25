# File:  RMAKHIJA_APATANKA_code.py

#####################################
# THIS IS ASSIGNMENT # 2........... #
#####################################

# This python script will read JSON data of traffic violations in Montgomery county directly from the source and
# then plot various histograms and maps to visualise the data.


# To run:
# python RMAKHIJA_APATANKA_code.py

# Source(s):
# The following url is used as a source for this code:
# https://www.dataquest.io/blog/python-json-tutorial/

# NOTE: Tabbing will create indented lines of code.

# Following packages are imported
import json
import urllib2
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium import plugins

#Follwing is the url for data
url = "https://data.montgomerycountymd.gov/api/views/4mse-ku6q/rows.json"

# this takes a python object and dumps it to a string which is a JSON
# representation of that object
# Extracting data from json file using json and urllib2
json = json.load(urllib2.urlopen(url))

# All columns from data
columns = json['meta']['view']['columns']

# Actual data which is neede from yhe json file
mdata = json['data']

# Column Names of the data
column_names = [col["fieldName"] for col in columns]

# Selecting the good columns from all the columns of data
good_columns = [
    "date_of_stop", "time_of_stop", "agency", "subagency","description","location", "latitude", "longitude",
    "vehicle_type", "year", "make", "model", "color", "violation_type","race", "gender", "driver_state",
    "driver_city", "dl_state","arrest_type"
]

# Creating useful data in a list
data = []
for row in mdata:
    selected_row = []
    for item in good_columns:
        selected_row.append(row[(column_names.index(item))])
    data.append(selected_row)

# Creating a data frame of useful data using pandas
stops = pd.DataFrame(data, columns=good_columns)

print stops

# Converting longitudes and latitudes to float
def parse_float(x):
    try:
        x = float(x)
    except Exception:
        x = 0
    return x
stops["longitude"] = stops["longitude"].apply(parse_float)
stops["latitude"] = stops["latitude"].apply(parse_float)

# Converting seperate columns of date and time to a single datetime float column
import datetime
def parse_full_date(row):
    date = datetime.datetime.strptime(row["date_of_stop"], "%Y-%m-%dT%H:%M:%S")
    time = row["time_of_stop"].split(":")
    date = date.replace(hour=int(time[0]), minute = int(time[1]), second = int(time[2]))
    return date
stops["date"] = stops.apply(parse_full_date, axis=1)

# Plotting histogram using matplotlib for number of traffic stops on a particular day and saving it as Figure 1
plt.hist(stops["date"].dt.weekday, bins=6, color = "red", ec = "black")
plt.xlabel("Weekdays: where 0: Monday & 6: Sunday")
plt.ylabel("Frequency")
plt.title("Histogram for Number of traffic stops on a particular day of a week")
plt.savefig('Figure1.png')
plt.show()
# Output can be seen below in Figure 1

# Plotting histogram using matplotlib for number of traffic stops on a particular time of day and saving it as Figure 2
plt.hist(stops["date"].dt.hour, bins=24, color = "red", ec = "black")
plt.xlabel("Time: where 0:12 a.m")
plt.ylabel("Frequency")
plt.title("Histogram for Number of traffic stops on a particular time of a day")
plt.savefig('Figure2.png')
plt.show()
# Output can be seen below in Figure 2

# Subsetting the data of last year
last_year = stops[stops["date"] > datetime.datetime(year=2016, month=2, day=18)]

# Subsetting the data of last years morning rush
morning_rush = last_year[(last_year["date"].dt.weekday < 5) & (last_year["date"].dt.hour > 5) & (last_year["date"].dt.hour < 10)]

# Mapping traffic stops on Montgomery county map using folium package
stops_map = folium.Map(location=[39.0836, -77.1483], zoom_start=11)
marker_cluster = folium.MarkerCluster().add_to(stops_map)
for name, row in morning_rush.iloc[:1000].iterrows():
    folium.Marker([row["latitude"], row["longitude"]], popup=row["description"]).add_to(marker_cluster)
stops_map.save('stops.html')
# Output can be seen down in Figure 3

# Creting a heatmap using folium package
stops_heatmap = folium.Map(location=[39.0836, -77.1483], zoom_start=11)
stops_heatmap.add_child(plugins.HeatMap([[row["latitude"], row["longitude"]] for name, row in morning_rush.iloc[:1000].iterrows()]))
stops_heatmap.save('heatmap.html')
# Output can be seen down in Figure 4

