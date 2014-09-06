# @file main.coffee
# @brief Defines the routes and javascript events for the gitorial app

gitorial = {};

# Templating
gitorial.templates =
    profile: Handlebars.compile $("#profile-template").html()
    edit: Handlebars.compile $("#edit-template").html()
    view: Handlebars.compile $("#view-template").html()
    home: Handlebars.compile $("#home-template").html()

# Routing
gitorial.routes = 
    profile: (params) ->
        address = '/api/' + params[0]
        console.log "profile:", address
        $.getJSON address, (data) -> 
            console.log data
            $('#container').html gitorial.templates.profile(data) 

    edit: (params) ->
        address = '/api/' + params[0] + '/' + params[1]
        console.log "edit:", address
        $.getJSON address, (data) -> 
            console.log data
            $('#container').html gitorial.templates.edit(data) 

    view: (params) ->
        address = '/api/' + params[0] + '/' + params[1]
        $.getJSON address, (data) -> 
            console.log data
            $('#container').html gitorial.templates.view(data) 

    home: ->
        $('#container').html gitorial.templates.home()

gitorial.router = ->
    route = location.hash[1..]
    [username, tutname, editflag] = route.replace(/\/$/, '').split('/')[1..];
    console.log username, tutname, editflag
    if editflag? and editflag == "edit" 
        gitorial.routes.edit [username, tutname]
    else if tutname? 
        gitorial.routes.view [username, tutname]
    else if username? 
        gitorial.routes.profile [username]
    else 
        gitorial.routes.home()

# call router
gitorial.router()
$(window).on 'hashchange', gitorial.router

# export gitorial
$(window).gitorial = gitorial
