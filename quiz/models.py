from django.db import models


class CategoryQuestion(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Answer(models.Model):
    name = models.CharField(max_length=200)
    explanation = models.TextField()
    code = models.TextField()
    category = models.ForeignKey(CategoryQuestion)

    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    code = models.TextField()
    category = models.ForeignKey(CategoryQuestion)
    correct_answer = models.ForeignKey(Answer)
    user_answer = None

    def __str__(self):
        return self.name


class Quiz():
    def __init__(self, n=2):
        self.questions = Question.objects.all()[:n]

    def __str__(self):
        return 'Set of Questions'


class UsefulLinks(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    link = models.CharField(max_length=200)
