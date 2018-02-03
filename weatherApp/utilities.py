from django.core.mail import send_mail

import requests

from .models import User

from klaviyo.settings import WUNDERGROUND_API_KEY, BASE_DIR

# http://api.wunderground.com/api/761cf5ce0fbe75e7/almanac/q/OH/Columbus.json
# http://api.wunderground.com/api/761cf5ce0fbe75e7/conditions/q/CA/San_Francisco.json

# Current Condition Phrases glossary
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
        if record['cur_temp'] - 5.0 >= record['almanac_avg_temp'] or record['cur_weather'] == 'Clear':
            subject = "It's nice out! Enjoy a discount on us."
            msg = populate_msg('good', record, city, state)
        elif record['cur_temp'] + 5.0 <= record['almanac_avg_temp'] or record['cur_weather'] in FULL_PRECIPITATING:
            subject = "Not so nice out? That's okay, enjoy a discount on us."
            msg = populate_msg('bad', record, city, state)
        else:
            subject = "Enjoy a discount on us."
            msg = populate_msg('normal', record, city, state)

        ''' User Django API to sent out emails'''
        print 'Successfully sent to ' + str(user.email) + ": " + str(user.location)
        send_mail(subject, msg, "klaviyo2018junbo@gmail.com", recipient, fail_silently=False)

def populate_msg(grade, record, city, state):
    """
    Description: Populate message filed.
    @para:
        type grade str: indication of good, normal or bad
        type record dict: contains weather info
        type city str: subscriber's city
        type state str: subscriber's state
    @ret:
        type msg str: cutomized message based on given info.
    """
    if grade == 'good':
        msg = "Hi there, we find out that the weather in {},{} is {}, and the degree is {} F. At this awesome weather, please enjoy our discount!".format(city, state, record['cur_weather'], record['cur_temp'])
    elif grade == 'bad':
        msg = "Hi there, we find out that the weather in {},{} is {}, and the degree is {} F. Since the weather is not so good, why don't come and check out our discount!".format(city, state, record['cur_weather'], record['cur_temp'])
    else:
        msg = "Hi there, we find out that the weather in {},{} is {}, and the degree is {} F. Come and enjoy our discount!".format(city, state, record['cur_weather'], record['cur_temp'])
    return msg


import os
from email.mime.image import MIMEImage
from django.conf import settings
from django.core import mail

def add_img(src, img_id):
    """
    :param src:
    :param img_id:
    :return:
    """
    fp = open(src, 'rb')
    msg_image = MIMEImage(fp.read())
    fp.close()
    msg_image.add_header('Content-ID', '<'+img_id+'>')
    return msg_image


def send_util():
    path = os.getcwd()
    path_use = path.replace('\\', '/')
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
        YOU FUCKING AWESOME
        <img src="cid:test_cid"/>
    </body>
    </html>
    '''
    recipient_list = ['junbo.li@duke.edu']
    from_mail = settings.EMAIL_HOST_USER
    msg = mail.EmailMessage('TEST TEST TEST', html, from_mail, recipient_list)
    msg.content_subtype = 'html'
    msg.mixed_subtype = 'related' # add image inline instead of as attachments
    msg.encoding = 'utf-8'
    image = add_img(BASE_DIR+'/puppy.jpg', 'test_cid')
    msg.attach(image)
    if msg.send():
        return True
    else:
        return False
