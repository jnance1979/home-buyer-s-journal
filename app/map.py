import requests
import pandas as pd
import folium
import os

def create_map(user_address):

    API_KEY = os.getenv('API_KEY')          # API call to google for geocoding data 

    params = {
        'key': API_KEY,
        'address': user_address
    }

    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'

    response = requests.get(base_url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        geometry = data['results'][0]['geometry']['location']
        viewport = data['results'][0]['geometry']['viewport']
        ne_lat = viewport['northeast']['lat']
        sw_lat = viewport['southwest']['lat']
        ne_lon = viewport['northeast']['lng']
        sw_lon = viewport['southwest']['lng']
        lat = geometry['lat']                       # determination of lat/lon coordinates
        lon = geometry['lng']


    else:
        print('No record for that address. Please try again.')
        return False

    chi_df = pd.DataFrame()             # establishment of empty dataframes in the event of error response from city database
    div_df = pd.DataFrame()
    pol_df = pd.DataFrame()
    fire_df = pd.DataFrame()
    lib_df = pd.DataFrame()
    cafe_df = pd.DataFrame()

    APP_TOKEN = os.getenv('APP_TOKEN')

    base_url = f'https://data.cityofchicago.org/resource/x2n5-8w5q.json?$$app_token={APP_TOKEN}&$where=within_circle(location, {lat}, {lon}, 400)'
    try:
        response = requests.get(base_url, None)     
        chi = response.json()
        chi_df = pd.DataFrame.from_records(chi)     # creation of reported crime dataframe
        if chi:
            chi_df.drop(['case_', '_iucr', 'arrest', 'domestic', 'beat', 'ward', 'fbi_cd', 'x_coordinate', 'y_coordinate', 'location'], axis=1, inplace=True)
    except:
        pass

    base_url = f'https://data.cityofchicago.org/resource/bbyy-e7gq.json?$$app_token={APP_TOKEN}&$where=within_circle(location, {lat}, {lon}, 800)'
    try:
        response = requests.get(base_url, None)
        div = response.json()
        div_df = pd.DataFrame.from_records(div)     # creation of Divvy bike dataframe
        if div:
            div_df.drop(['id', 'location'], axis=1, inplace=True)
    except:
        pass

    base_url = f'https://data.cityofchicago.org/resource/z8bn-74gv.json?$$app_token={APP_TOKEN}&$where=within_circle(location, {lat}, {lon}, 800)'
    try:    
        response = requests.get(base_url, None)
        pol = response.json()
        pol_df = pd.DataFrame.from_records(pol)     # creation of police station dataframe
        if pol:
            pol_df.drop(['website', 'fax', 'tty', 'x_coordinate', 'y_coordinate', 'location'], axis=1, inplace=True)
    except:
        pass

    base_url = f'https://data.cityofchicago.org/resource/28km-gtjn.json?$$app_token={APP_TOKEN}&$where=within_circle(location, {lat}, {lon}, 800)'
    try:
        response = requests.get(base_url, None)
        fire = response.json()
        fire_df = pd.DataFrame.from_records(fire)   # creation of fire station dataframe
    except:
        pass

    base_url = f'https://data.cityofchicago.org/resource/x8fc-8rcq.json?$$app_token={APP_TOKEN}&$where=within_circle(location, {lat}, {lon}, 800)'
    try:
        response = requests.get(base_url, None)
        lib = response.json()
        lib_df = pd.DataFrame.from_records(lib)     # creation of library dataframe
    except:
        pass

    base_url = f"https://data.cityofchicago.org/resource/nxj5-ix6z.json?$$app_token={APP_TOKEN}&$where=within_circle(location, {lat}, {lon}, 400)"
    try:
        response = requests.get(base_url, None)
        cafe = response.json()
        cafe_df = pd.DataFrame.from_records(cafe)   # creation of sidewalk cafe dataframe
    except:
        pass

  
    this_map = folium.Map(prefer_canvas=True)       # creation of map

    def plotDot(point):
        folium.CircleMarker(location=[point.latitude, point.longitude],
                            tooltip=f'{point.date_of_occurrence} : {point._primary_decsription}',
                            color='red',
                            radius=3,
                            weight=5).add_to(this_map)      # creation of crime markers

    chi_df.apply(plotDot, axis = 1)
 

    def plotDot(point):
        folium.CircleMarker(location=[point.latitude, point.longitude],
                            tooltip=f'Divvy Station: {point.station_name}; status: {point.status}',
                            color = 'lightblue',
                            radius=15,
                            weight=10).add_to(this_map)     # creation of Divvy markers

    div_df.apply(plotDot, axis = 1)


    def plotDot(point):
        folium.CircleMarker(location=[point.latitude, point.longitude],
                            tooltip=f'Police Station District: {point.district}; address: {point.address}',
                            color = 'blue',
                            radius=15,
                            weight=10).add_to(this_map)     # creation of police station markers

    pol_df.apply(plotDot, axis = 1)


    def plotDot(point):
        folium.CircleMarker(location=[point.location['latitude'], point.location['longitude']],
                            tooltip=f'Fire Station: Engine: {point.engine}; address: {point.address}',
                            color = 'red',
                            radius=15,
                            weight=10).add_to(this_map)     # creation of fire station markers
    
    fire_df.apply(plotDot, axis = 1)


    def plotDot(point):
        folium.CircleMarker(location=[point.location['latitude'], point.location['longitude']],
                            tooltip=f'Library: {point.name_}; address: {point.address}',
                            color = 'green',
                            radius=15,
                            weight=10).add_to(this_map)     # creation of library markers

    lib_df.apply(plotDot, axis = 1)


    def plotDot(point):
        folium.CircleMarker(location=[point.location['latitude'], point.location['longitude']],
                            tooltip=f'Sidewalk Cafe: {point.doing_business_as_name}; address: {point.address}',
                            color = 'yellow',
                            radius=5,
                            weight=10).add_to(this_map)     # creation of sidewalk cafe markers

    cafe_df.apply(plotDot, axis = 1)



    folium.Marker(location=[lat, lon],
                        tooltip=f'{user_address}',
                        weight=5).add_to(this_map)      # creation of user address marker


    this_map.fit_bounds(this_map.get_bounds())

    this_map.save( 'app/templates/map_output.html' )    # save map to file in templates folder
