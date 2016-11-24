from django.db import models


class G(object):
    pass


class CategoryQuestion(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    code = models.TextField()
    category = models.ForeignKey(CategoryQuestion)
    user_answer = None

    def __str__(self):
        return self.name


class Answer(models.Model):
    name = models.CharField(max_length=200)
    explanation = models.TextField()
    code = models.TextField()
    question = models.ForeignKey(Question)
    correct_answer = models.BooleanField(default=False)

    def __str__(self):
        return 'Name: ' + str(self.name) + '   Is correct: ' + str(self.correct_answer)



class Quiz():
    def __init__(self, n=2):
        self.questions = Question.objects.all()[:n]
        for k, v in enumerate(self.questions):
            self.questions[k].answers = frozenset(Answer.objects.filter(question=v.id))
            self.questions[k].correct_answers = {k.id for k in self.questions[k].answers if k.correct_answer }

    def __str__(self):
        return 'Set of Questions'


class UsefulLinks(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    link = models.CharField(max_length=200)
