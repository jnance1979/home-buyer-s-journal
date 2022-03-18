from urllib import response
import requests
import pandas as pd
# import numpy as np
# from sodapy import Socrata
# import geocoder
import folium
import os
# user_address = input('Enter the address >')

##################################################################
# df = pd.read_csv('./Crimes_-_One_year_prior_to_present.csv')
def create_map(user_address):

    API_KEY = os.getenv('API_KEY')

    params = {
        'key': API_KEY,
        'address': user_address
    }

    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'


    response = requests.get(base_url, params=params)
    data = response.json()


    if data['status'] == 'OK':
        geometry = data['results'][0]['geometry']['location']
        lat = geometry['lat']
        lon = geometry['lng']
        # print(f'lat:{lat}   lon:{lon}')
    else:
        print('No record for that address. Please try again.')
        return False

    # crimes = df[(df['LATITUDE'] >= (lat - .005)) & (df['LATITUDE'] <= (lat + .005)) & (df['LONGITUDE'] <= (lon + .005)) & (df['LONGITUDE'] >= (lon - .005))]
    # print(crimes.head())


    n_lat = (lat + .002)
    s_lat = (lat - .002)
    e_lon = (lon + .002)
    w_lon = (lon - .002)


    base_url = f'https://data.cityofchicago.org/resource/x2n5-8w5q.json?$where=latitude>{s_lat} AND latitude<{n_lat} AND longitude<{e_lon} AND longitude>{w_lon}'


    response = requests.get(base_url, None)
    chi = response.json()
    chi_df = pd.DataFrame.from_records(chi)
    if chi:
        chi_df.drop(['case_', '_iucr', 'arrest', 'domestic', 'beat', 'ward', 'fbi_cd', 'x_coordinate', 'y_coordinate', 'location'], axis=1, inplace=True)


    base_url = f'https://data.cityofchicago.org/resource/bbyy-e7gq.json?$where=latitude>{lat - .005} AND latitude<{lat + .005} AND longitude<{lon + .005} AND longitude>{lon - .005}'

    response = requests.get(base_url, None)
    div = response.json()
    div_df = pd.DataFrame.from_records(div)
    if div:
        div_df.drop(['id', 'location'], axis=1, inplace=True)


    #create a map
    this_map = folium.Map(prefer_canvas=True)

    def plotDot(point):
        folium.CircleMarker(location=[point.latitude, point.longitude],
                            tooltip=f'{point.date_of_occurrence} : {point._primary_decsription}',
                            color='red',
                            radius=3,
                            weight=5).add_to(this_map)

    chi_df.apply(plotDot, axis = 1)


    def plotDot(point):
        folium.CircleMarker(location=[point.latitude, point.longitude],
                            tooltip=f'Divvy Station: {point.station_name}; status: {point.status}',
                            color = 'lightblue',
                            radius=15,
                            weight=10).add_to(this_map)

    div_df.apply(plotDot, axis = 1)


    folium.Marker(location=[lat, lon],
                        tooltip=f'{user_address}',
                        weight=5).add_to(this_map)


    this_map.fit_bounds(this_map.get_bounds())

    #Save the map to an HTML file
    this_map.save( 'app/templates/map_output.html' )


    # print(f'Crimes occurring within a 1 block area:\n')
    # print(chi_df.sort_values(by=['latitude'], ascending=False))
    # print(f'\n Divvy Stations within a 1 kilometer area:\n')
    # print(div_df.head())
