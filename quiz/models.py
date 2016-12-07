from django.db import models
from  django.core.validators import validate_comma_separated_integer_list

from datetime import datetime, timedelta
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
    answers = models.TextField(default='буде помилка / error \nжодне з перелічених / none of the mentioned')
    correct_answer = models.CharField(max_length=10, validators=[validate_comma_separated_integer_list])
    explanation = models.TextField(blank=True, default='Спробуйте і переконайтеся.')
    enabled = models.BooleanField(default=False)

    user_answer = {None}

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



class Quiz():
    def __init__(self):
        self.questions = []
        self.categories = CategoryQuestion.objects.all()
        for category in self.categories[:1]:
            lst = list(Question.objects.all().filter(enabled=True).filter(category=category.id))
            shuffle(lst)
            self.questions.extend(lst[-2:])

        self.start_time = datetime.now()
        self.stop_time = datetime.now()
        self.time_delta = self.stop_time - self.start_time

    def __str__(self):
        return 'Set of Questions'

    def result(self):
        list_result = [v.get_correct_answer() == v.user_answer for v in self.questions]
        c_a = list_result.count(True)  # correct answers
        w_a = list_result.count(False)  # wrong answers
        n_a = c_a + w_a
        k = round(c_a / n_a * 100)
        data_result = [c_a, w_a, n_a, k, k >= 80]
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
