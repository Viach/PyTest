from django.contrib import admin

from .models import Question, Answer, CategoryQuestion, UsefulLinks

admin.site.register(CategoryQuestion)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UsefulLinks)