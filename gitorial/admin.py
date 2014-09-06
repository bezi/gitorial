from django.contrib import admin
from gitorial.models import User, Tutorial, Step, Commit, File, Line

admin.site.register(User)
admin.site.register(Tutorial)
admin.site.register(Step)
admin.site.register(Commit)
admin.site.register(File)
admin.site.register(Line)
