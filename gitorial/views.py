from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext

import json

# Create your views here.
def index(request):
  return render_to_response('index.html', 
      {}, 
      context_instance=RequestContext(request))

def user(request, username):
    tutorial_data = {}
    tutorial_data['title'] = 'tutorial title'
    tutorial_data['description'] = 'Super duper cool tutorial'
    tutorial_data['url'] = '#/view/bezi/tutorial'

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
