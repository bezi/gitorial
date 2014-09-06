from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template import RequestContext
import django.contrib.auth
import social.apps.django_app.views

import json

# Create your views here.
def index(request):
  return render_to_response('index.html', 
      {}, 
      context_instance=RequestContext(request))

def session(request):
  if request.method == 'POST':
    social.apps.django_app.views.auth(request, 'github')

  elif request.method == 'GET':
    if(request.user is not None and
       request.user.is_authenticated()):
      user = {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'last_login': request.user.last_login,
        'email': request.user.email,
        'id': request.user.id,
        'pk': request.user.pk
      }

      # I can't find an attribute for pictures.
      # We can either get this manually (with the API itself),
      # or I might be able to figure it out with python-social-auth

      print('---')
      print('\n'.join(dir(request.user)))
      print('---')
    else:
      user = False

    return HttpResponse(json.dumps({
          'user': user
        }),
        content_type="application/json")
    
  elif request.method == 'DELETE':
    django.contrib.auth.logout(request)
    return HttpResponse()

  else:
    return HttpResponseNotAllowed(['POST', 'GET', 'DELETE'])

def user(request, username):
    tutorial_a = {}
    tutorial_a['title'] = 'Javascript Quirks'
    tutorial_a['description'] = 'Super duper weird things about Javascript you should know.'
    tutorial_a['url'] = '#/' + username + '/1'

    tutorial_b = {}
    tutorial_b['title'] = 'CSS Tricks'
    tutorial_b['description'] = 'Handy dandy CSS tricks that you can use in your next website'
    tutorial_b['url'] = '#/' + username + '/2'

    repo_data = {}
    repo_data['name'] = username + '/cmueats'
    repo_data['description'] = 'It\'s for finding food!'
    repo_data['url'] = 'github.com/' + username + '/cmueats'

    response_data = {}
    response_data['name'] = None
    response_data['username'] = username
    response_data['avatar_url'] = 'http://placekitten.com/400/400'
    response_data['is_owner'] = True
    response_data['tutorials'] = [tutorial_a, tutorial_b]
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

    diff = {}
    diff['diff_url'] = "http://www.google.com"
    diff['code_url'] = "http://www.facebook.com"
    diff['files'] = [file_res]

    step = {}
    step['title'] = 'step_title'
    step['content_before'] = 'not too'
    step['diff'] = diff
    step['content_after'] = 'hard to see what this does'

    response = {}
    response['id'] = 543125
    response['title'] = 'tutorial title'
    response['description'] = 'shizzles mach nizzles'
    response['repo_url'] = 'github.com/here/it/is'
    response['is_editable'] = True
    response['steps'] = [step]
    
    return HttpResponse(json.dumps(response), content_type="application/json")
