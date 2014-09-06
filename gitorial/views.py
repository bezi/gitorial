from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext

import json

# Create your views here.
def index(request):
  print(request.user.username)
  print(request.user.first_name)
  print(request.user.last_name)
  print(request.user.last_login)
  print(request.user.email)
  print(request.user.id)
  print(request.user.pk)
  print(type(request.user))
  # I can't find an attribute for pictures.
  # We can either get this manually (with the API itself),
  # or I might be able to figure it out with python-social-auth

  print('---')

  print('\n'.join(dir(request.user)))

  return render_to_response('index.html', 
      {user: str(dir(request.user))}, 
      context_instance=RequestContext(request))

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
    line = {}
    line['number'] = 33
    line['content'] = 'int i = 3;'
    line['addition'] = True
    line['deletion'] = False

    file_res = {}
    file_res['name'] = "assign.c"
    file_res['lines'] = [line]

    commit = {}
    commit['commit_url'] = "http://www.google.com"
    commit['code_url'] = "http://www.facebook.com"
    commit['files'] = [file_res]

    step = {}
    step['title'] = 'step_title'
    step['content_before'] = 'not too'
    step['commit'] = commit
    step['content_after'] = 'hard to see what this does'

    response = {}
    response['id'] = 543125
    response['title'] = 'tutorial title'
    response['description'] = 'shizzles mach nizzles'
    response['repo_url'] = 'github.com/here/it/is'
    response['is_editable'] = True
    response['steps'] = [step]
    
    return HttpResponse(json.dumps(response), content_type="application/json")
