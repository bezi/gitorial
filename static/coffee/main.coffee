router = ->
  route = location.hash[1..]
  [endpoint, params...] = route.split('/')[1..]
  switch endpoint
    when 'home' then renderHome params
    when 'profile' then renderProfile params
    when 'edit' then renderEdit params
    when 'view' then renderView params
  return

renderHome = (params) ->
  templateSource = $("#home-template").html()
  template = Handlebars.compile templateSource
  $('#container').html template()

fakeProfileData =
  name: 'Tom Shen'
  avatar_url: 'https://avatars0.githubusercontent.com/u/2065456?v=2&s=460'
  if_current_url: true
  tutorials: [
    {
      name: 'JavaScript Quirks'
      url: '#/view/javascriptquirks'
    }
    {
      name: 'CSS Tricks'
      url: '#/view/csstricks'
    }
  ]

renderProfile = (params) ->
  templateSource = $("#profile-template").html()
  template = Handlebars.compile templateSource
  $('#container').html template(fakeProfileData)

fakeTutorialData =
  title: 'JavaScript Quirks'
  steps: [
    {
      title: 'Undefined vs null'
      content_before: 'Use null in your code'
      content_after: 'Undefined is used to show absence of value, not null values'
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