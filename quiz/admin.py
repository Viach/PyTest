from django.contrib import admin

from .models import Question, CategoryQuestion, UsefulLinks

admin.site.register(CategoryQuestion)
admin.site.register(Question)
admin.site.register(UsefulLinks)