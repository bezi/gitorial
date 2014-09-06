from django.shortcuts import render
from django.http import HttpResponse

import json

def user(request, username):
    response_data = {}
    response_data['name'] = 'Tom Shen'
    response_data['username'] = username
    response_data['avatar_url'] = 'http://placekitten.com/400/400'
    response_data['is_owner'] = True
    response_data['tutorial'] = []
    response_data['repos'] = []
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")
