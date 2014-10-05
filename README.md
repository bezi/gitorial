# gitorial

## What
Gitorial is a webapp that takes github repos and builds tutorial blogs from them.  See it live at [gitorial.com](gitorial.com).

## Installation
If you want, like, explanations for what's going on in this setup (i.e., you don't just believe that I speak the truth), you can read [here][getting-started] for more information.

We're using python 3.4, so make sure you have it.

### Setting up virtualenvwrapper
```bash
# If you don't already have virtualenvwrapper:
$ pip install virtualenvwrapper

# If you haven't already, add the following lines to your bash/zsh config:
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
# Now source that file (or logout/login again)
```

### Setting up the gitorial virtualenv
Virtualenv's are used so that python dependencies don't bleed from one project into another.

```bash
mkvirtualenv --python=`which python3` gitorial
# Your shell prompt should have been prepended with (gitorial)
# The virtualenv you just created is _yours_, i.e. if you want to make a
# special prompt for it or give it a special name, you can. Read the docs.
```

Some notes about working in virtualenvs: if (gitorial) is in your prompt, you are in the virtualenv. This means that all the dependencies are in place, all the python versions are taken care of, etc. If you need to stop working on the virtualenv (i.e., to make another one, make a temporary testing environment, or stop working on gitorial for the day) run `deactivate`.

To work on a virtualenv once it has been created (i.e., when you open up a fresh terminal), run `workon gitorial`.


#### Installing Django (for future reference, YOU DON'T HAVE TO DO THIS)
This is here because it's chronologically when I ran the commands when setting up the project. They __only need to be run once__.

```bash
pip install django
django-admin.py startproject gitorial
manage.py startapp gitorial
```

### First-time Setup
These commands, unlike in the previous section, will need to be run once for every user the first time after clonining this repo.

```bash
# Make sure that you are working on the (gitorial) virtualenv

# Installs Django (v1.7 omg sho kewl)
pip install -r requirements.txt

# Sets up the database (new in Django 1.7 omg sho kewl)
./manage.py migrate

# Install CoffeeScript (if you haven't already)
npm install -g coffee-script
```


[getting-started]: http://www.jeffknupp.com/blog/2013/12/18/starting-a-django-16-project-the-right-way/
