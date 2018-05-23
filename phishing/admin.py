from django.contrib import admin

# Register your models here.

from .models import MTurkUser, Submission, Constraint, Rating

admin.site.register(MTurkUser)
admin.site.register(Rating)
admin.site.register(Constraint)
admin.site.register(Submission) 
