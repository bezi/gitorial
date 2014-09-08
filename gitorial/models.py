from django.db import models

from jsonfield import JSONField

class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, primary_key=True)
    avatar_url = models.CharField(max_length=100)
    last_updated = models.DateTimeField(null=True)

    def getDict(self):
      return {
          'name': self.name,
          'username': self.username,
          'avatar_url': self.avatar_url,
          'last_updated': str (self.last_updated)
      }

    def __str__(self):
        return self.name + ' (' + self.username + ')'

class Tutorial(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    repo_name = models.CharField(max_length=100)
    repo_url = models.CharField(max_length=100)
    owner = models.ForeignKey(User)
    def __str__(self):
        return self.title

class Step(models.Model):
    index = models.IntegerField()
    title = models.CharField(max_length=100)
    content_before = models.TextField()
    content_after = models.TextField()

    diff_url = models.CharField(max_length=250)
    code_url = models.CharField(max_length=250)

    files = models.TextField()

    tutorial = models.ForeignKey(Tutorial)
    def __str__(self):
        return self.title
