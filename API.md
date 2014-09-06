/api/user/_username_
-------
Github metadata to allow us to build a profile page.

GET:
```
response = {
    name: 'Tom Shen' // full name
    username: 'tomshen' // github username
    avatar_url: 'https:blah' // avatar
    is_owner: true // true if requested by this user
    tutorials : [
        {
            title: 'tutorial title',
            description: 'Super duper cool tutorial'
            url: '#/view/bezi/tutorial'
        }
    ]
}
```
GET, POST, DELETE

if the person has never signed in with us, return nothing.

If the person is the same as the person logged in, also add:
```
    repos : [
        {
            name: 'name of repo'
            description: 'the repo description from github'
            url: 'github.com/tomshen/shizzlesforrizzles'
        }
        ]
```

/api/_user-name_/_tut-name_/
---
GET:
```
response = {
    id: 21341234134
    title: 'tutorial title'
    description: 'shizzles mah nizzles'
    repo_url: 'github.com/here/it/is'
    is_editable: true // true if requested by owner
    steps: [
        title: 'step_title'
        content_before: 'not too'
        commit: {
            commit_url:
            code_url:
            files: [
                {
                    name:
                    lines: [
                        {
                            number: 33
                            content: "int i = 3;"
                            addition: true/false
                            deletion: true/false
                        }
                    ]
                }
            ]
        }
        content_after: 'hard to see what this does'
    ]
}
```

POST:
```
request = {
    github_url: asdfsadf
    }
response = {
    tutorial_url: szdf
}
```

DELETE:

PATCH:
request: same as get
