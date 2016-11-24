from django.db import models


class G(object):
    pass


class CategoryQuestion(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    code = models.TextField(blank=True)
    category = models.ForeignKey(CategoryQuestion)
    user_answer = None

    def __str__(self):
        return self.name


class Answer(models.Model):
    name = models.CharField(max_length=200)
    explanation = models.TextField(blank=True)
    code = models.TextField(blank=True)
    question = models.ForeignKey(Question)
    correct_answer = models.BooleanField(default=False)

    def __str__(self):
        return 'Name: ' + str(self.name) + '   Is correct: ' + str(self.correct_answer)



class Quiz():
    def __init__(self, n=2):
        self.questions = Question.objects.all()[:n]
        for k, v in enumerate(self.questions):
            self.questions[k].answer = frozenset(Answer.objects.filter(question=v.id))
            self.questions[k].correct_answer = set(k.id for k in self.questions[k].answer if k.correct_answer )
            self.questions[k].input_type = 'radio' if len(self.questions[k].correct_answer) == 1 else 'checkbox'

    def __str__(self):
        return 'Set of Questions'

    def result(self):
        return [v.correct_answer == v.user_answer for v in self.questions]


class UsefulLinks(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    link = models.CharField(max_length=200)
