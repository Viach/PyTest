from django.db import models

class CategoryQuestion(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

class Answer(models.Model):
    name = models.CharField(max_length=200)
    explanation = models.TextField()
    code = models.TextField()
    category = models.ForeignKey(CategoryQuestion)

class Question(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    code = models.TextField()
    category = models.ForeignKey(CategoryQuestion)
    correct_answer = models.ForeignKey(Answer)

class UsefulLinks(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    link = models.CharField(max_length=200)
