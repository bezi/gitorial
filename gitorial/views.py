from django.core import serializers
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden,HttpResponseNotModified, HttpResponseNotFound
from django.template import RequestContext
from gitorial.models import User, Tutorial, Step, Commit
import django.contrib.auth
import social.apps.django_app.views
import json
import requests
from config import settings
from datetime import datetime, timedelta

import diff

# Create your views here.
def index(request):
  return render_to_response('index.html', {},
      context_instance=RequestContext(request))

def logout(request):
  django.contrib.auth.logout(request)
  return redirect('/')

def session(request):
  if request.method == 'GET':
    if(request.user is not None and
       request.user.is_authenticated()):
      username = request.user.username
    else:
      username = ''

    return HttpResponse(json.dumps({
          'username': username
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
    except:
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

def build_steps(username, repo_name, tutorial, commits_data):
    steps = []
    for commit_data in commits_data:
        step, is_new = Step.objects.get_or_create(tutorial=tutorial)
        if is_new:
            step.title = commit_data['title']
            step.content_before = commit_data['message']
            step.content_after = ''
            step.commit = build_commit(username, repo_name, commit_data)
            step.save()
        steps.append(step)
    return steps

def build_commit(username, repo_name, commit_data):
    commit, is_new = Commit.objects.get_or_create(step=commit_data['step'])
    if is_new:
        commit.diff_url = commit_data['diff_url']
        commit.code_url = commit_data['code_url']
        api_r = requests.get(
            'https://api.github.com/users/%s/%s/commits/%s?client_id=%s&client_secret=%s' % (
                username,
                repo_name,
                commit_data['sha'],
                settings.SOCIAL_AUTH_GITHUB_KEY,
                settings.SOCIAL_AUTH_GITHUB_SECRET
            ))
        print(api_r.headers['X-RateLimit-Remaining'])
        commit.files = diff.parse(api_r.text)
        commit.save()
    return commit

def tutorial_new(request, username, repo):
  if request.method == 'POST':
    try:
      user = User.objects.get(username=username)

      repo_r = requests.get('https://api.github.com/repos/%s/%s?client_id=%s&client_secret=%s' % (username, repo, settings.SOCIAL_AUTH_GITHUB_KEY, settings.SOCIAL_AUTH_GITHUB_SECRET))
      repo_r_json = repo_r.json()

      tut_entry, is_new = Tutorial.objects.get_or_create(id=repo_r_json['id'])
      if not is_new:
        return HttpResponseForbidden()
      else:
        tut_entry.title = repo_r_json['title']
        tut_entry.description = repo_r_json['description']
        tut_entry.repo_url = repo_r_json['url']
        tut_entry.owner = user
        tut_entry.save()

        commits_r = requests.get(repo_r_json['commits_url'].replace('{/sha}', '') + ('?client_id=%s&client_secret=%s' % (settings.SOCIAL_AUTH_GITHUB_KEY, settings.SOCIAL_AUTH_GITHUB_SECRET)))
        commits_r_json = commits_r.json()

        commits_data = []
        for commit in commits_r_json:
          (title_raw, _, message_raw) = commit.message.partition('\n')[0][:50]

          results.append({
            'sha': commit.sha,
            'title': title_raw[:50],
            'message': message_raw,
            'diff_url': commit.html_url,
            'code_url': 'https://github.com/%s/%s/tree/%s' % (username, repo, commit.sha)
          })

        commits_data.sort(reverse=True)

        build_steps(username, repo, tut_entry, commits_data)

        return HttpResponse(json.dumps({
          'tutorial_id': tut_entry.id
          }),
          content_type="application/json")
    except:
      return HttpResponseNotFound('No such user with username.')
  else:
    return HttpResponseNotAllowed(['POST'])

def tutorial(request, username, tutnum):
  if request.method == 'GET':
    # tut is an ID (number)
    tut_entry = Tutorial.objects.get(id=tutnum)
    response = {'id': tutnum,
                'title': tut_entry.title,
                'description': tut_entry.description,
                'repo_url': tut_entry.repo_url,
                'steps': build_steps(tut_entry) 
               }

    return HttpResponse(json.dumps(response), content_type="application/json")
  elif request.method == 'DELETE':
    return HttpResponse(status="501")
  elif request.method == 'PATCH':
    return HttpResponse(status="501")
  else:
    return HttpResponseNotAllowed(['POST','GET'])

