from django.core import serializers
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from gitorial.models import User, Tutorial, Step, Commit, File, Line
import django.contrib.auth
import json

# Create your views here.
def index(request):
  if(request.user is not None and request.user.is_authenticated()):
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
    user = None

  return render_to_response('index.html', 
      {'gitorial_user': user}, 
      context_instance=RequestContext(request))

def logout(request):
  django.contrib.auth.logout(request)
  return redirect('/')

def user(request, username):
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
