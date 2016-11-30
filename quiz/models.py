from django.db import models
from  django.core.validators import validate_comma_separated_integer_list

from  random import shuffle


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
    answers = models.TextField()
    correct_answer = models.CharField(max_length=10, validators=[validate_comma_separated_integer_list])
    explanation = models.TextField(blank=True)

    user_answer = None

    def __str__(self):
        return self.name

    def get_answers(self):
        list_answers = self.answers.split('\r\n')
        list_answers = [[k, v] for k, v in zip(range(1, len(list_answers) + 1), list_answers)]
        shuffle(list_answers)
        return list_answers

    def get_correct_answer(self):
        return {int(i) for i in self.correct_answer.split(',')}

    def get_input_type(self):
        return 'radio' if len(self.get_correct_answer()) == 1 else 'checkbox'


class G(object):
    def __init__(self):
        # delete all children for G class
        pass

    def __str__(self):
        return 'My Global Object'


class Quiz():
    def __init__(self, n=25):
        self.questions = Question.objects.all()[:n]

    def __str__(self):
        return 'Set of Questions'

    def result(self):
        list_result = [v.get_correct_answer() == v.user_answer for v in self.questions]
        c_a = list_result.count(True)
        w_a = list_result.count(False)
        k = round(c_a / (c_a + w_a) * 100)
        data_result = [c_a, w_a, k, k >= 80]
        return [list_result, data_result]


class UsefulLinks(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class EMail():
    def __init__(self):
        self.subject = 'Заголовок'

    def __str__(self):
        return 'Email from Guest'