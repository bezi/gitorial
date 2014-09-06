router = ->
  route = location.hash[1..]
  [endpoint, params...] = route.split('/')[1..]
  switch endpoint
    when 'home' then renderHome params
    when 'profile' then renderProfile params
    when 'edit' then renderEdit params
    when 'view' then renderView params
    when '404' then renderNotFound params
  $('textarea').autosize()
  return

renderNotFound = (params) ->
  templateSource = $("#not-found-template").html()
  template = Handlebars.compile templateSource
  $('#container').html template()

renderHome = (params) ->
  templateSource = $("#home-template").html()
  template = Handlebars.compile templateSource
  $('#container').html template({
    username: 'profile'
    is_logged_in: true
  })

fakeProfileData =
  name: 'Tom Shen'
  username: 'tomshen'
  avatar_url: 'https://avatars0.githubusercontent.com/u/2065456?v=2&s=460'
  is_owner: true
  tutorials: [
    {
      title: 'JavaScript Quirks'
      description: 'Super duper weird things about JavaScript you should know'
      url: '#/view/javascriptquirks'
    }
    {
      title: 'CSS Tricks'
      description: 'Handy dandy CSS tricks that you can use in your next website'
      url: '#/view/csstricks'
    }
  ]

renderProfile = (params) ->
  templateSource = $("#profile-template").html()
  template = Handlebars.compile templateSource
  $('#container').html template(fakeProfileData)

fakeTutorialData =
  user: {
    name: 'Tom Shen'
    username: 'tomshen'
  }
  is_owner: true
  title: 'JavaScript Quirks'

  steps: [
    {
      title: 'Undefined vs null'
      content_before: 'Use null in your code'
      content_after: 'Undefined is used to show absence of value, not null values'
      diff:
        diff_url: 'https://github.com/bezi/gitorial/commit/e6952684c670180d667fed6e640ada148f197dba'
        code_url: 'https://github.com/bezi/gitorial/tree/e6952684c670180d667fed6e640ada148f197dba'
        files: [
          {
            name: 'static/coffee/main.coffee'
            lines: [
              {
                number: 42
                content: "     username: 'tomshen'"
              }
              {
                number: 43
                content: "     avatar_url: 'https://avatars0.githubusercontent.com/u/2065456?v=2&s=460'"
                deletion: true
              }
              {
                number: 44
                content: "   }"
              }
              {
                number: 45
                content: "   is_owner: true"
                addition: true
              }
            ]
          }
          {
            name: 'static/coffee/main.coffee'
            lines: [
              {
                number: 42
                content: "     username: 'tomshen'"
              }
              {
                number: 43
                content: "     avatar_url: 'https://avatars0.githubusercontent.com/u/2065456?v=2&s=460'"
                deletion: true
              }
              {
                number: 44
                content: "   }"
              }
              {
                number: 45
                content: "   is_owner: true"
                addition: true
              }
            ]
          }
        ]
    }
    {
      title: '=== vs =='
      content_before: '== is incredibly inconsistent. Never use it.'
      content_after: 'Always use ===, since it will never implicitly do type conversion.'
    }
  ]

renderEdit = (params) ->
  templateSource = $("#edit-template").html()
  template = Handlebars.compile templateSource
  $('#container').html template(fakeTutorialData)

renderView = (params) ->
  templateSource = $("#view-template").html()
  template = Handlebars.compile templateSource
  $('#container').html template(fakeTutorialData)

$(window).on 'hashchange', router



if '#' in location.hash
  router()
