from django.shortcuts import render
from .models import Quiz


def index(request):
    context = {'var': 'quiz index.html', }
    return render(request, 'quiz/index.html', context)


def quiz(request):
    if request.session.get('quiz_status', None) == "start":
        request.session['current_question'] = 1
        request.session['quiz_status'] = 'process'
    else:
        request.session['quiz_status'] = 'finish'

    quiz = Quiz()
    context = {'quiz': quiz, 'test': 'TEST'}
    return render(request, 'quiz/quiz.html', context)


def useful_links(request):
    context = {'var': 'quiz LINKS', }
    return render(request, 'quiz/useful_links.html', context)
