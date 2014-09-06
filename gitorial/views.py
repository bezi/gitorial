from django.core import serializers
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template import RequestContext
from gitorial.models import User, Tutorial, Step, Commit, File, Line
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
    user_entry = User.objects.get(username=username.strip('/'))
    response = {'name': user_entry.name,
                'username': user_entry.username,
                'avatar_url': user_entry.avatar_url,
                'is_owner': False,
                'tutorials': build_tutorials(user_entry)}
    return HttpResponse(json.dumps(response), content_type="application/json")

def build_tutorials(user):
    user_tutorials = Tutorial.objects.filter(owner=user).values('title', 'description', 'repo_url').order_by('id').reverse()
    return [{'title': item['title'],
             'description': item['description'],
             'url': item['repo_url']}
            for item in user_tutorials]

def tutorial(request, username, tutnum):
    tut_entry = Tutorial.objects.get(id=tutnum)
    response = {'id': tutnum,
                'title': tut_entry.title,
                'description': tut_entry.description,
                'repo_url': tut_entry.repo_url,
                'is_editable': False,
                'steps': build_steps(tut_entry) 
               }

    return HttpResponse(json.dumps(response), content_type="application/json")

def build_steps(tutorial):
    return [{'title': item.title,
             'content_before': item.content_before,
             'content_after': item.content_after,
             'commit': build_commit(item)
            }
            for item in Step.objects.filter(tutorial=tutorial).order_by('id')]

def build_commit(step):
    commit = Commit.objects.get(step=step)
    return {'diff_url': commit.diff_url,
            'code_url': commit.code_url,
            'files': build_files(commit)}

def build_files(commit):
    commit_files = File.objects.filter(commit=commit).order_by('name')
    return [{'name': item.name,
             'lines': build_lines(item)} 
            for item in commit_files]

def build_lines(src_file):
    file_lines = Line.objects.filter(src_file=src_file).order_by('number')
    return [{'number': item.number,
             'content': item.content,
             'addition': item.addition,
             'deletion': item.deletion} 
             for item in file_lines]
