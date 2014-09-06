# @file main.coffee
# @brief Defines the routes and javascript events for the gitorial app

gitorial = {};

# Session
gitorial.session =
    update: ->
        $.ajax
            dataType: 'json'            
            type: 'GET'
            async: false
            url: '/api/session/'
            headers: 
                'x-csrftoken' : $.cookie 'csrftoken'
        .done (data) ->
            gitorial.session.session = data
        .fail gitorial.routes.fail

    login: ->
        $.ajax
            dataType: 'json'            
            type: 'POST'
            url: '/api/session/'
            headers: 
                'x-csrftoken' : $.cookie 'csrftoken'
        .done gitorial.session.update

    logout: ->
        $.ajax
            dataType: 'json'            
            type: 'DELETE'
            url: '/api/session/'
            headers: 
                'x-csrftoken' : $.cookie 'csrftoken'
        .done gitorial.session.update
        
    session: null

# Templating
gitorial.templates =
    profile: Handlebars.compile $("#profile-template").html()
    edit: Handlebars.compile $("#edit-template").html()
    view: Handlebars.compile $("#view-template").html()
    home: Handlebars.compile $("#home-template").html()
    fail: Handlebars.compile $("#not-found-template").html()

# Routing
gitorial.routes = 
    profile: (params) ->
        address = '/api/' + params[0] + '/'
        $.ajax
            dataType: 'json'
            url: address
            type: 'GET'
            headers: 
                'x-csrftoken' : $.cookie 'csrftoken'
        .done (data) ->
            $('#container').html gitorial.templates.profile(data) 
        .fail ->
            $.ajax
                dataType: 'json'
                url: address
                headers: 
                    'x-csrftoken' : $.cookie 'csrftoken'
                type: 'POST'
            .done gitorial.router
            .fail gitorial.fail

    edit: (params) ->
        address = '/api/' + params[0] + '/' + params[1] + '/'
        $.ajax
            dataType: 'json'
            url: address
            headers: 
                'x-csrftoken' : $.cookie 'csrftoken'
            type: 'GET'
        .done (data) ->
            $('#container').html gitorial.templates.edit(data) 
        .fail gitorial.routes.fail
            

    view: (params) ->
        address = '/api/' + params[0] + '/' + params[1] + '/'
        $.ajax
            dataType: 'json'
            url: address
            headers:
                'x-csrftoken' : $.cookie 'csrftoken'
            type: 'GET'
        .done (data) ->
            $('#container').html gitorial.templates.view(data) 
        .fail gitorial.routes.fail

    home: ->
        $('#container').html gitorial.templates.home()

    fail: ->
        $('#container').html gitorial.templates.fail()

gitorial.router = ->
    route = location.hash[1..]
    [username, tutname, editflag] = route.replace(/\/$/, '').split('/')[1..];
    if editflag? and editflag == "edit" 
        gitorial.routes.edit [username, tutname]
    else if tutname? 
        gitorial.routes.view [username, tutname]
    else if username? 
        gitorial.routes.profile [username]
    else 
        gitorial.routes.home()

# attach listeners to errythang

# call router
gitorial.router()
$ window 
.on 'hashchange', gitorial.router

# export gitorial
window.gitorial = gitorial
