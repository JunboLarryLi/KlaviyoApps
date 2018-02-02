from django.core.mail import send_mail

import requests

from .models import User

'''
TODO: move to WUNDERGROUND_API_KEY into settings, but given import name error
'''
WUNDERGROUND_API_KEY = '761cf5ce0fbe75e7'


# 'http://api.wunderground.com/api/761cf5ce0fbe75e7/almanac/q/OH/Columbus.json'
# 'http://api.wunderground.com/api/761cf5ce0fbe75e7/conditions/q/CA/San_Francisco.json'
def weather_data(city, state):
    """
    Description: Apply Wundergound API to retrieve weather record for a given location.
    @para:
        type city str: subscriber's city
        type state str: subscriber's state
    ret:
        type: dict  {
                        key1: calculated historical average temperature
                        key2: current temperature
                        key3: current weather
                    }
    """
    link_almanac = 'http://api.wunderground.com/api/{}/almanac/q/{}/{}.json'.format(WUNDERGROUND_API_KEY, state, city)
    link_cur = 'http://api.wunderground.com/api/{}/conditions/q/{}/{}.json'.format(WUNDERGROUND_API_KEY, state, city)

    '''
    Calculate historical average temperature'''
    almanac_weather_record = requests.get(link_almanac).json()
    if 'almanac' in almanac_weather_record:
        history_high = float(almanac_weather_record['almanac']['temp_high']['normal']['F'])
    else:
        history_high = cur_temp
    if 'almanac' in almanac_weather_record:
        history_low = float(almanac_weather_record['almanac']['temp_low']['normal']['F'])
    else:
        history_low = cur_temp
    almanac_avg_temp = (history_low + history_high)/2

    ''' Retrieve current temperature'''
    cur_weather_record = requests.get(link_cur).json()
    cur_temp = cur_weather_record['current_observation']['temp_f']
    cur_weather = cur_weather_record['current_observation']['weather']

    return {'almanac_avg_temp': almanac_avg_temp, 'cur_temp': cur_temp, 'cur_weather': cur_weather}

def send_emails():
    """
    Description: Apply SendGrid API to send newsletters to all subscribers from our database.
    @para: None
    ret: None.
    """
    subject = ""
    msg = ""
    recipient = []
    users = User.objects.all()
    for user in users:
        recipient = [user.email]
        geography = user.location.split(',')
        city, state = geography[0], geography[1]
        record = weather_data(city, state)

        ''' Populate subject filed'''
        if record['cur_temp'] - 5.0 >= record['almanac_avg_temp'] or record['cur_weather'] == 'Sunny':
            subject = "It's nice out! Enjoy a discount on us."
        elif record['cur_temp'] + 5.0 <= record['almanac_avg_temp']:
            subject = "Not so nice out? That's okay, enjoy a discount on us."
        else:
            subject = "Enjoy a discount on us."

        ''' Populate message filed'''
        msg = "Hi there, we find out that the weather in {},{} is {}, and the degree is {} F. Time to enjoy our discount!".format(city, state, record['cur_weather'], record['cur_temp'])

        ''' User Django API to sent out emails'''
        print 'Successfully sent to ' + str(user.email) + ": " + str(user.location)
        send_mail(subject, msg, "klaviyo2018junbo@gmail.com", recipient, fail_silently=False)
