from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea

from .models import Question, CategoryQuestion, UsefulLinks

admin.site.register(CategoryQuestion)


class QuestionAdmin(admin.ModelAdmin):
    fields = [ 'name', 'code', 'category', 'answers', 'correct_answer', 'explanation', 'enabled']
    list_display = ['name', 'category', 'enabled', ]
    list_editable = ['enabled', ]
    list_filter = ['enabled', 'category', ]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '80'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 5, 'cols': 80})},
    }


admin.site.register(Question, QuestionAdmin)

admin.site.register(UsefulLinks)
