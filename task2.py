'''
This module create a web-map, where you can choose some layer(filter) to see\
    info about films and places, where they were taken.
'''
from ast import arg
import csv
import folium
from geopy.geocoders import Nominatim, ArcGIS
from functools import lru_cache
from geopy import distance

arcgis = ArcGIS(timeout=10)
nominatim = Nominatim(timeout=10, user_agent="justme")

import argparse
parser = argparse.ArgumentParser(description='')
parser.add_argument('year', type=str)
parser.add_argument('latitude', type=str)
parser.add_argument('longtitude', type=str)
parser.add_argument('filepath', type=str)
args = parser.parse_args()

geocoders = [arcgis, nominatim]

@lru_cache(maxsize=None)
def geocode(address):
    '''
    Return coordinates, where address take place
    >>> print(geocode('Aeroporto, Lisbon, Portugal'))
    (38.88560396835856, -9.038366756931474)
    '''
    i = 0
    try:
        location = geocoders[i].geocode(address)
        # print(location)
        if location != None:
            return location.latitude, location.longitude
        i += 1
        location = geocoders[i].geocode(address)
        # print(location)
        if location != None:
            return location.latitude, location.longitude
    except:
        return None

def read_file(path: str) -> list :
    '''
    Return list of lines from file
    '''
    info = []
    with open(path, 'r',encoding='utf-8',errors='ignore') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for content in csv_reader:
            # if '2017' in content[1]:
            if args.year in content[1]:
                location = content[-1]
                coords = geocode(location)
                if coords:
                    latitude, longtitude = coords
                    content.append((latitude, longtitude))
                    info.append(content)
    return info

def find_distance(first_cords, second_cords):
    '''
    Find distance between two places
    >>> print(find_distance((49.83826, 24.02324), (59.83826, 80.02324)))
    2263.1124948155843
    '''
    my_distance = distance.distance(first_cords, second_cords).miles
    return my_distance

def find_min_max_distance(contain):
    '''
    Find 10 closest and 10 farest places 
    '''
    dict_for_top = {}
    second_cords = (float(args.latitude), float(args.longtitude))
    # second_cords = (49.83826, 24.02324)
    for line in contain:
        result = find_distance(second_cords, line[-1])
        dict_for_top[(line[0], line[-1])] = result
    min_sorted = sorted(dict_for_top.items(), key=lambda x: x[1])
    max_sorted = sorted(dict_for_top.items(), key=lambda x: x[1], reverse = True)
    only_films_min = [el[0] for el in min_sorted]
    if len(only_films_min) >= 10:
        list_films_ten_min = only_films_min[:10]
    only_films_max = [el[0] for el in max_sorted]
    if len(only_films_max) >= 10:
        list_films_ten_max = only_films_max[:10]
    return list_films_ten_min, list_films_ten_max

def europe_area(contain):
    '''
    Define if place locate in Europe
    >>> print(europe_area([['A Outra', '(2008)',\
        'Aeroporto, Lisbon, Portugal', (38.88560396835856, -9.038366756931474)]]))
    [('A Outra', (38.88560396835856, -9.038366756931474))]
    '''
    europe_countries = []
    for line in contain:
        # print(line)
        if 36.0 <= line[-1][0] <= 71.08:
            if -9.34 <= line[-1][1] <= 67.20:
                europe_countries.append((line[0], line[-1]))
    return europe_countries

def web_work(res_min, res_max, europe_countries):
    '''
    Make layers and markers for web-map
    '''
    map = folium.Map(location=[float(args.latitude), float(args.longtitude)])
    fg_hc = folium.FeatureGroup(name="10 closest")

    for pair in res_min:
        fg_hc.add_child(folium.Marker(location=[pair[1][0], pair[1][1]],
            popup = f"Film name: {pair[0]}",
            icon=folium.Icon(color = 'pink')))

    fg_ln = folium.FeatureGroup(name="10 farest")

    for pair in res_max:
        fg_ln.add_child(folium.Marker(location=[pair[1][0], pair[1][1]],
            popup = f"Film name: {pair[0]}",
            icon=folium.Icon(color = 'green')))

    fg_all = folium.FeatureGroup(name="Film in Europe")
    for pair in europe_countries:
        fg_all.add_child(folium.Marker(location=[pair[1][0], pair[1][1]],
            radius = 10,
            popup = f"Film name: {pair[0]}",
            color = 'cyan',
            fill_opacity = 0.5))
    map.add_child(fg_all)
    map.add_child(fg_hc)
    map.add_child(fg_ln)
    map.add_child(folium.LayerControl())
    map.save('Films.html')

if __name__ == "__main__":
    contain = read_file(args.filepath)
    res_min, res_max = find_min_max_distance(contain)
    europe_countries = europe_area(contain)
    web_work(res_min, res_max, europe_countries)
    import doctest
    doctest.testmod()

