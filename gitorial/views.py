from django.core import serializers
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden,HttpResponseNotModified, HttpResponseNotFound
from django.template import RequestContext
from gitorial.models import User, Tutorial, Step, Commit, File, Line
import django.contrib.auth
import social.apps.django_app.views
import json
import requests
from config import settings
from datetime import datetime, timedelta

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

def user_view(request, username):
  if request.method =='POST':
    user, is_new = User.objects.get_or_create(username=username)

    if is_new:
      api_r = requests.get('https://api.github.com/users/%s?client_id=%s&client_secret=%s' % (username, settings.SOCIAL_AUTH_GITHUB_KEY, settings.SOCIAL_AUTH_GITHUB_SECRET))

      # Log how many requests are remaining
      print(api_r.headers['X-RateLimit-Remaining'])

      response_json = api_r.json()

      try:
        user.name = response_json['name']
      except:
        pass
      user.avatar_url = response_json['avatar_url']
      user.last_modified = datetime.now()
      user.save()

      return HttpResponse(status=201)
    else:
      return HttpResponseForbidden()

  elif request.method =='GET':
    try:
      user = User.objects.get(username=username)

      return HttpResponse(json.dumps({
        'user': user.getDict()
      }),
      content_type="application/json")
    except:
      return HttpResponseNotFound()

  elif request.method =='DELETE':
    try:
      User.objects.get(username=username).delete()
      return HttpResponse()
    except DoesNotExist:
      return HttpResponseNotFound()

  elif request.method =='PATCH':
    try:
      user = User.objects.get(username=username)

      if (datetime.now() - user.last_modified) > timedelta(hours=1):
        api_r = requests.get('https://api.github.com/users/%s?client_id=%s&client_secret=%s' % (username, settings.SOCIAL_AUTH_GITHUB_KEY, settings.SOCIAL_AUTH_GITHUB_SECRET))

        # Log how many requests are remaining
        print(api_r.headers['X-RateLimit-Remaining'])

        response_json = api_r.json()

        try:
          user.name = response_json['name']
        except:
          pass
        user.avatar_url = response_json['avatar_url']
        user.last_modified = datetime.now()
        user.save()

        return HttpResponse()
      else:
        return HttpResponseNotModified()
    except DoesNotExist:
      return HttpResponseNotFound()

  else:
    return HttpResponseNotAllowed(['POST', 'GET', 'DELETE'])

  user_entry = User.objects.get(username=username.strip('/'))
  user_tutorials = Tutorial.objects.filter(owner=user_entry).values('title', 'description', 'repo_url')
  response = {'name': user_entry.name,
              'username': user_entry.username,
              'avatar_url': user_entry.avatar_url,
              'is_owner': False,
              'tutorials': [{'title': item['title'],
                             'description': item['description'],
                             'url': item['repo_url']} 
                             for item in user_tutorials]}
  return HttpResponse(json.dumps(response), content_type="application/json")

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
