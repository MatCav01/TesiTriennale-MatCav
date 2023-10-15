from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

import iot_api_client as iot

# client id and secret
my_client_id = "CLIENT_ID"
my_client_secret = "CLIENT_SECRET"

# Get your token 
oauth_client = BackendApplicationClient(client_id=my_client_id)
token_url = "https://api2.arduino.cc/iot/v1/clients/token"

oauth = OAuth2Session(client=oauth_client)
token = oauth.fetch_token(
    token_url=token_url,
    client_id=my_client_id,
    client_secret=my_client_secret,
    include_client_id=True,
    audience="https://api2.arduino.cc/iot",
)

# store access token in access_token variable
access_token = token.get("access_token")

# configure and instance the API client with our access_token
client_config = iot.Configuration(host="https://api2.arduino.cc/iot")
client_config.access_token = access_token
client = iot.ApiClient(client_config)

# api instance
api = iot.PropertiesV2Api(client)

# ids
thing_id = "THING_ID"
# device_id = "DEVICE_ID"

switch_id = 'SWITCH_ID'
speed_id = 'SPEED_ID'
direction_id = 'DIRECTION_ID'
temperature_id = 'TEMPERATURE_ID'
humidity_id = 'HUMIDITY_ID'

try:
    exit = False
    while not exit:
        param = input('''\nType the parameter of the motor to modify (switch, speed, direction),
                      type \"humidity\" to print the last value of humidity,
                      type \"temperature\" to print the timeseries data of temperature
                      or type \"exit\" to exit the program: ''').lower()
        if param == 'switch':
            switch = input('Type the value of the switch (ON, OFF): ').upper()
            if switch == 'ON':
                api.properties_v2_publish(thing_id, switch_id, property_value={'value': True})
            elif switch == 'OFF':
                api.properties_v2_publish(thing_id, switch_id, property_value={'value': False})
        
        elif param == 'speed':
            speed = input('Type the value of the speed (1, 2, 3): ')
            if speed == '1':
                api.properties_v2_publish(thing_id, speed_id, property_value={'value': 155})
            elif speed == '2':
                api.properties_v2_publish(thing_id, speed_id, property_value={'value': 205})
            elif speed == '3':
                api.properties_v2_publish(thing_id, speed_id, property_value={'value': 255})
            
       
        elif param == 'direction':
            direction = input('Type the value of the direction (forward, reverse): ').lower()
            if direction == 'forward':
                api.properties_v2_publish(thing_id, direction_id, property_value={'value': 0})
            if direction == 'reverse':
                api.properties_v2_publish(thing_id, direction_id, property_value={'value': 1})

        elif param == 'temperature':
            lower = input('Type the timestamp of the lower border: ')
            upper = input('Type the timestamp of the upper border: ')
            interval = input('Type the time interval (in seconds): ')
            if input('Type \"YES\" if you want the values in descendent time order: ').upper() == 'YES':
                desc = True
            else:
                desc = False
            
            temp_timeseries = api.properties_v2_timeseries(thing_id, temperature_id, desc=desc, _from=lower, interval=interval, to=upper)
            print('\n#\tDatetime\t\t\tTemperature')
            for i in range(0, len(temp_timeseries.data)):
                print(i + 1, temp_timeseries.data[i].time, temp_timeseries.data[i].value, sep='\t', end=' ')
                print('°C')

        elif param == 'humidity':
            humidity = api.properties_v2_show(thing_id, humidity_id)
            print('\nHumidity: ', humidity.last_value, '%', sep='')

        elif param == 'exit':
            exit = True

except iot.ApiException as e:
    print("Got an exception: {}".format(e))
