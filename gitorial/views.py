from django.core import serializers
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden,HttpResponseNotModified, HttpResponseNotFound, JsonResponse
from django.template import RequestContext
from gitorial.models import User, Tutorial, Step
import django.contrib.auth
import social.apps.django_app.views
import json
import requests
from config import settings
from datetime import datetime, timedelta

from . import diff

# Create your views here.
def index(request):
    return render_to_response('index.html', {},
            context_instance=RequestContext(request))

def logout(request):
    django.contrib.auth.logout(request)
    return redirect('/')

def callback(request):
    if(request.user is not None and
         request.user.is_authenticated()):
        return redirect('/#/' + request.user.username)
    else:
        return redirect('/')
    return

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
    if request.method == 'POST':
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
            result = user.getDict()

            if request.user.username == username:
                repo_r = requests.get('https://api.github.com/users/%s/repos?client_id=%s&client_secret=%s&sort=pushed' % (username, settings.SOCIAL_AUTH_GITHUB_KEY, settings.SOCIAL_AUTH_GITHUB_SECRET))
                repo_r_json = repo_r.json()

                result['repos'] = [{
                    'title': repo['name'],
                    'description': repo['description']
                } for repo in repo_r_json]

            result['tutorials'] = [{
                'id': tutorial.id,
                'title': tutorial.title,
                'description': tutorial.description,
                'repo_url': tutorial.repo_url
            } for tutorial in Tutorial.objects.filter(owner=user)]

            return HttpResponse(json.dumps(result),
                    content_type="application/json")
        except Exception as e:
            print(e)
            return HttpResponseNotFound()

    elif request.method == 'DELETE':
        try:
            User.objects.get(username=username).delete()
            return HttpResponse()
        except Exception as e:
            print(e)
            return HttpResponseNotFound()

    elif request.method == 'PATCH':
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
        except Exception as e:
            print(e)
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
    index = 0
    for commit_data in commits_data:
        index += 1
        step, is_new = Step.objects.get_or_create(index=index, tutorial=tutorial)
        if is_new:
            step.title = commit_data['title']
            step.content_before = commit_data['message']
            step.content_after = ''

            step.diff_url = commit_data['diff_url']
            step.code_url = commit_data['code_url']

            api_r = requests.get(
                'https://api.github.com/repos/%s/%s/commits/%s?client_id=%s&client_secret=%s' % (
                    username,
                    repo_name,
                    commit_data['sha'],
                    settings.SOCIAL_AUTH_GITHUB_KEY,
                    settings.SOCIAL_AUTH_GITHUB_SECRET
                    ), headers={'Accept': 'application/vnd.github.diff'})

            step.files = json.dumps(diff.parse(api_r.text))

            step.save()

def tutorial_new(request, username, repo):
    if request.method == 'POST':
        user = User.objects.get(username=username)

        repo_r_json = requests.get(
            'https://api.github.com/repos/%s/%s?client_id=%s&client_secret=%s' % (
              username,
              repo,
              settings.SOCIAL_AUTH_GITHUB_KEY,
              settings.SOCIAL_AUTH_GITHUB_SECRET)
        ).json()

        tut_entry, is_new = Tutorial.objects.get_or_create(id=repo_r_json['id'], owner = user)

        tut_entry.title = repo_r_json['name']
        tut_entry.description = repo_r_json['description']

        tut_entry.repo_name = repo_r_json['name']
        tut_entry.repo_url = repo_r_json['url']

        tut_entry.owner = user
        tut_entry.save()

        # Get all commits, most recent first
        commits_r_json = requests.get(
            repo_r_json['commits_url'].replace('{/sha}', '') +
            ('?client_id=%s&client_secret=%s' % (
              settings.SOCIAL_AUTH_GITHUB_KEY,
              settings.SOCIAL_AUTH_GITHUB_SECRET))
        ).json()

        commits_data = []
        for commit in commits_r_json:
            (title_raw, _, message_raw) = commit['commit']['message'].partition('\n')

            commits_data.insert(0, {
                'sha': commit['sha'],
                'title': title_raw[:50],
                'message': message_raw,
                'diff_url': commit['html_url'],
                'code_url': 'https://github.com/%s/%s/tree/%s' % (username, repo, commit['sha'])
            })

        build_steps(username, repo, tut_entry, commits_data)

        return JsonResponse({'tutorial_id': tut_entry.id}) 
    else:
        return HttpResponseNotAllowed(['POST'])

def tutorial(request, username, tutnum):
    if request.method == 'GET':
        # tut is an ID (number)
        tut_entry = Tutorial.objects.get(id=tutnum)

        response = {
            'id': tutnum,
            'title': tut_entry.title,
            'description': tut_entry.description,
            'repo_name': tut_entry.repo_name,
            'repo_url': tut_entry.repo_url,
            'steps': [{
                'title': step.title,
                'content_before': step.content_before,
                'content_after': step.content_after,
                'diff_url': step.diff_url,
                'code_url': step.code_url,
                'files': json.loads(step.files)
            } for step in Step.objects.filter(tutorial=tutnum).order_by('index')]
        }

        return JsonResponse(response)
    elif request.method == 'DELETE':
        # tut is an ID (number)
        Tutorial.objects.get(id=tutnum).delete()
        return HttpResponse()
    elif request.method == 'PATCH':
        patch = json.loads(request.body)
        try:
            tut_entry = Tutorial.objects.get(id=tutnum)

            tut_entry.title = patch['title']
            tut_entry.description = patch['description']
            tut_entry.save()

            index = 0
            for step_json in patch['steps']:
                index += 1
                step = Step.objects.get(tutorial=tut_entry, index=index)

                step.title = patch[index - 1]['title']
                step.content_before = patch[index - 1]['content_before']
                step.content_after = patch[index - 1]['content_after']
                step.save()
        except Tutorial.DoesNotExist:
            return HttpResponseNotFound()
    else:
        return HttpResponseNotAllowed(['POST','GET','DELETE','PATCH'])

