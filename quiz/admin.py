from django.contrib import admin

from .models import Question, CategoryQuestion, UsefulLinks

admin.site.register(CategoryQuestion)


class QuestionAdmin(admin.ModelAdmin):
    #fields = ['name', 'enabled']
    list_filter = ['enabled']


admin.site.register(Question, QuestionAdmin)


admin.site.register(UsefulLinks)
