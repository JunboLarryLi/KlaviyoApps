import os

import requests
from email.mime.image import MIMEImage
from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string

from klaviyo.settings import WUNDERGROUND_API_KEY, BASE_DIR
from .models import User


'''
Reference/links of the Wundergound API
'''
# http://api.wunderground.com/api/761cf5ce0fbe75e7/almanac/q/OH/Columbus.json
# http://api.wunderground.com/api/761cf5ce0fbe75e7/conditions/q/CA/San_Francisco.json

'''
Current Condition Phrases glossary
'''

# https://www.wunderground.com/weather/api/d/docs?d=resources/phrase-glossary&MR=1
PRECIPITATING = set(
    ['Drizzle',
    'Rain',
    'Snow',
    'Snow Grains',
    'Ice Crystals',
    'Ice Pellets',
    'Hail',
    'Mist',
    'Fog',
    'Fog Patches',
    'Smoke',
    'Volcanic Ash',
    'Widespread Dust',
    'Sand',
    'Haze',
    'Spray',
    'Dust Whirls',
    'Sandstorm',
    'Low Drifting Snow',
    'Low Drifting Widespread Dust',
    'Low Drifting Sand',
    'Blowing Snow',
    'Blowing Widespread Dust',
    'Blowing Sand',
    'Rain Mist',
    'Rain Showers',
    'Snow Showers',
    'Snow Blowing Snow Mist',
    'Ice Pellet Showers',
    'Hail Showers',
    'Small Hail Showers',
    'Thunderstorm',
    'Thunderstorms and Rain',
    'Thunderstorms and Snow',
    'Thunderstorms and Ice Pellets',
    'Thunderstorms with Hail',
    'Thunderstorms with Small Hail',
    'Freezing Drizzle',
    'Freezing Rain',
    'Freezing Fog'])

FULL_PRECIPITATING = set()
for phrase in PRECIPITATING:
    FULL_PRECIPITATING.add(phrase)
    FULL_PRECIPITATING.add('Light ' + phrase)
    FULL_PRECIPITATING.add('Heavy ' + phrase)


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
    Description: Apply SendGrid API to send newsletters(in html template) to all subscribers from our database.

    @para: None

    ret: None
    """
    subject = ""
    from_mail = settings.EMAIL_HOST_USER
    users = User.objects.all()

    for user in users:
        context = {}
        recipient_list = [user.email]
        geography = user.location.split(',')
        city, state = geography[0], geography[1]
        record = weather_data(city, state)

        ''' Populate subject filed'''
        if record['cur_temp'] - 5.0 >= record['almanac_avg_temp'] or record['cur_weather'] == 'Clear':
            subject = "It's nice out! Enjoy a discount on us."
            image = add_img(BASE_DIR + '/weatherApp/static/email_content_sunny.jpeg', 'weather')

        elif record['cur_temp'] + 5.0 <= record['almanac_avg_temp'] or record['cur_weather'] in FULL_PRECIPITATING:
            subject = "Not so nice out? That's okay, enjoy a discount on us."
            image = add_img(BASE_DIR + '/weatherApp/static/email_content_rain.jpeg', 'weather')

        else:
            subject = "Enjoy a discount on us."
            image = add_img(BASE_DIR + '/weatherApp/static/email_content_normal.jpeg', 'weather')


        context['city'] = city
        context['state'] = state
        context['weather'] = record['cur_weather']
        context['temperature'] = record['cur_temp']
        logo = add_img(BASE_DIR + '/weatherApp/static/klaviyo-logo.jpeg', 'klaviyo-logo')

        html_content = render_to_string(BASE_DIR + '/weatherApp/templates/newsletter.html', context=context).strip()
        msg = mail.EmailMessage(subject, html_content, from_mail, recipient_list)
        msg.content_subtype = 'html'    # Main content is text/html
        msg.mixed_subtype = 'related' # This is critical, otherwise images will be displayed as attachments!

        msg.attach(image)
        msg.attach(logo)

        ''' User Django API to sent out emails'''
        if msg.send():
            print 'Successfully sent to ' + str(user.email) + ": " + str(user.location)
        else:
            print 'Unsuccessfully sent to ' + str(user.email) + ": " + str(user.location)

def add_img(src, img_id):
    """
    Description: Wrap an image, used for sending inline image as a html email template 
    :param src:
    :param img_id:
    :return:
    """
    fp = open(src, 'rb')
    msg_image = MIMEImage(fp.read())
    fp.close()
    msg_image.add_header('Content-ID', '<'+img_id+'>')
    return msg_image
