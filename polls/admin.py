from django.contrib import admin

from .models import Question, UserEducation, Profile

admin.site.register(Question)
admin.site.register(UserEducation)
admin.site.register(Profile)
