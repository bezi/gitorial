# @file main.coffee
# @brief Defines the routes and javascript events for the gitorial app

window.gitorial = {}

# Session
gitorial.session =
    update: ->
        $.ajax
            dataType: 'json'
            type: 'GET'
            url: '/api/session/'
            headers:
                'x-csrftoken' : $.cookie 'csrftoken'
        .done (data) ->
            gitorial.session.username = data.username
            gitorial.session.loggedin = data.username isnt ""
            gitorial.router();
            return
        .fail gitorial.routes.fail
        return
        
    username: null
    loggedin: false

# Templating
gitorial.templates =
    profile: Handlebars.compile $("#profile-template").html()
    edit: Handlebars.compile $("#edit-template").html()
    view: Handlebars.compile $("#view-template").html()
    home: Handlebars.compile $("#home-template").html()
    fail: Handlebars.compile $("#not-found-template").html()

# Routing
gitorial.routes =
    home: ->
        data =
            gitorial: gitorial
        $('#container').html gitorial.templates.home data
        return

    tutorialPane: true

    profile: (params) ->
        address = '/api/' + params[0] + '/'
        $.ajax
            dataType: 'json'
            url: address
            type: 'GET'
            headers:
                'x-csrftoken' : $.cookie 'csrftoken'
        .done (data) ->
            data.isowner = gitorial.session.username is params[0]
            data.tutorialPane = gitorial.routes.tutorialPane
            data.reposPane = not data.tutorialPane
            data.gitorial = gitorial
            $('#container').html gitorial.templates.profile data
            $ '.new-tutorial-button'

            # Event listeners
            .on 'click', (e) ->
                gitorial.routes.tutorialPane = not gitorial.routes.tutorialPane
                gitorial.session.update()
                return

            $ '.user-listing-title'
            .on 'click', (e) -> 
                gitorial.tutorials.handleClick(e)
                return

            $ '#'

        .fail ->
            $.ajax
                dataType: 'json'
                url: address
                type: 'POST'
                headers:
                    'x-csrftoken' : $.cookie 'csrftoken'
            .done (data) ->
                gitorial.session.update()
                return
            .fail gitorial.routes.fail
        return

    edit: (params) ->
        address = '/api/' + params[0] + '/' + params[1] + '/'
        $.ajax
            dataType: 'json'
            url: address
            headers:
                'x-csrftoken' : $.cookie 'csrftoken'
            type: 'GET'
        .done (data) ->
            data.isowner = gitorial.session.username is params[0]
            data.gitorial = gitorial
            $('#container').html gitorial.templates.edit data
            gitorial.tutorials.data = data
            $('textarea').autosize()
            return
        .fail gitorial.routes.fail
        return
            
    view: (params) ->
        address = '/api/' + params[0] + '/' + params[1] + '/'
        $.ajax
            dataType: 'json'
            url: address
            headers:
                'x-csrftoken' : $.cookie 'csrftoken'
            type: 'GET'
        .done (data) ->
            data.isowner = gitorial.session.username is params[0]
            data.gitorial = gitorial
            $('#container').html gitorial.templates.view data
                
            return
        .fail gitorial.routes.fail
        return

    fail: ->
        $('#container').html gitorial.templates.fail()
        return

gitorial.router = ->
    route = location.hash[1..]
    [username, tutname, editflag] = route.replace(/\/$/, '').split('/')[1..]
    if editflag? and editflag == "edit"
        gitorial.routes.edit [username, tutname]
    else if tutname?
        gitorial.routes.view [username, tutname]
    else if username?
        gitorial.routes.profile [username]
    else
        gitorial.routes.home()
    return

# Tutorial generator utilities
gitorial.tutorials = {}
gitorial.tutorials =
    handleClick: (e) ->
        if not gitorial.routes.tutorialPane
            reponame = e.target.innerHTML
            user = gitorial.session.username
            $.ajax
                dataType: 'json'
                url: '/api/' + user + '/' + reponame + '/'
                type: 'POST'
                headers:
                    'x-csrftoken' : $.cookie 'csrftoken'
            .done (data) ->
                url = '/#/' + user + '/' + data.tutorial_id + '/edit'
                location.href = url
                gitorial.session.update()
                return
            .fail gitorial.routes.fail
        else
            reponame = e.target.innerHTML
            user = gitorial.session.username
            $.ajax
                dataType: 'json'
                url: '/api/' + user + '/' + reponame + '/'
                type: 'GET'
                headers:
                    'x-csrftoken' : $.cookie 'csrftoken'
            .done (data) ->
                url = '/#/' + user + '/' + data.tutorial_id + '/'
                location.href = url
                gitorial.session.update()
                return
            .fail gitorial.routes.fail
        return
    data: null

    save: ->
        # iterate over the ui, save into JSON
        saveData = 
            title: $(".tutorial-title").val()
            steps: $(".tutorial-step")
        
        $.ajax
            dataType: 'json'
            url: '/api/' + gitorial.session.username + '/' + gitorial.session.tutorial_id + '/'
            type: 'POST'
            data: gitorial.tutorials.data
        .done (data) ->
            console.log "Saved."
            return
        .fail
            console.log "Unable to save."
            return
        return
    
# call router
gitorial.session.update()

$ window
.on 'hashchange', gitorial.session.update

$ window
.on 'ready', gitorial.session.update
