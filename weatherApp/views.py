# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse

from django.conf import settings
import json
import os
import re

from django import forms
from .models import User
# from .utilities import send_util

STATES_HASH = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Federated States Of Micronesia': 'FM',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Marshall Islands': 'MH',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands': 'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Palau': 'PW',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

# Create your views here.

def index(request):
    f = os.path.join(settings.BASE_DIR, 'weatherApp/cities.json')
    data = json.load(open(f))
    top_100_cities = []
    for i in range(100):
        top_100_cities.append(data[i]['city']+", " + STATES_HASH[data[i]['state']])
    context = {}
    context['cities'] = top_100_cities
    return render(request, 'index.html', context)

'''
S1: Parse request
S2: Validate email address
    Case I: vaid email address -> Case a: if in DB -> go to another page
                                  Case b: not in DB -> add to DB & send confirmation & go to anther page
    Case II: invalid emall address -> html build-in will remind
'''
def subscribe(request):
    # send_util()
    # Parse loc & email
    user_email = request.POST.get("email", "")
    user_location = request.POST.get("location", "")

    # validate the email address, http://emailregex.com/
    emailregex = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if emailregex.match(user_email) == None:
        return render(request, 'invalid_email.html')

    # if in DB -> go to another page
    if len(User.objects.all().filter(email = user_email)) > 0:
        return render(request, 'already_registered_user.html')
    # if not in DB -> add to DB & send confirmation & go to anther page
    else:
        user = User(email = user_email, location = user_location)
        user.save()
        return render(request, 'success.html')
