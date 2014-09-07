from django.contrib import admin
from gitorial.models import User, Tutorial, Step, Commit

admin.site.register(User)
admin.site.register(Tutorial)
admin.site.register(Step)
admin.site.register(Commit)
