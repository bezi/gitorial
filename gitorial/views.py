from django.shortcuts import render
from django.http import HttpResponse

import json

def user(request, username):
    tutorial_data = {}
    tutorial_data['title'] = 'tutorial title'
    tutorial_data['description'] = 'Super duper cool tutorial'
    tutorial_data['url'] = '#/bezi/1010'

    repo_data = {}
    repo_data['name'] = 'name of repo'
    repo_data['description'] = 'the repo description from github'
    repo_data['url'] = 'github.com/tomshen/shizzlesforrizzles'

    response_data = {}
    response_data['name'] = 'Tom Shen'
    response_data['username'] = username
    response_data['avatar_url'] = 'http://placekitten.com/400/400'
    response_data['is_owner'] = True
    response_data['tutorials'] = [tutorial_data, tutorial_data]
    response_data['repos'] = [repo_data, repo_data, repo_data]

    
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def tutorial(request, username, tutname):
    return HttpResponse(username + ', ' + tutname)
