/api/user/_username_
-------
Github metadata to allow us to build a profile page.

GET:
```javascript
response = {
    name: 'Tom Shen' // full name
    username: 'tomshen' // github username
    avatar_url: 'https:blah' // avatar
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

```javascript
    repos : [
        {
            name: 'name of repo'
            description: 'the repo description from github'
            url: 'github.com/tomshen/shizzlesforrizzles'
        }
        ]
```

/api/_user-name_/_tut-num_/
---
GET:

```javascript
response = {
    id: 21341234134
    title: 'tutorial title'
    description: 'shizzles mah nizzles'
    repo_url: 'github.com/here/it/is'
    steps: [
        title: 'step_title'
        content_before: 'not too'
        content_after: 'hard to see what this does'
        diff_url:
        code_url:
        files: [
            {
                name:
                chunks: [
                    [
                        {
                            old_number: 33/undefined
                            new_number: 35/undefined
                            content: "int i = 3;"
                            addition: true/false/undefined
                            deletion: true/false/undefined
                        }
                    ]
                ]
            }
        ]
    ]
}
```

POST:

```javascript
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
