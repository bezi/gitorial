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
  return render_to_response('index.html', {}, 
      context_instance=RequestContext(request))

def logout(request):
  django.contrib.auth.logout(request)
  return HttpResponse()

def session(request):
  if request.method == 'GET':
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

    else:
      user = False

    return HttpResponse(json.dumps({
          'user': user
        }),
        content_type="application/json")

  else:
    return HttpResponseNotAllowed(['GET'])

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

      return HttpResponse(json.dumps(user.getDict()),
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
