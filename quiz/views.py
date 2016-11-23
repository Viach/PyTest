from django.shortcuts import render
from .models import Quiz

quiz = Quiz()


def index(request):
    context = {'var': 'quiz index.html', }
    return render(request, 'quiz/index.html', context)


def quiz(request):
    if request.session.get('quiz_status') == None:
        request.session['current_question'] = 0
        context = ''
        return render(request, 'quiz/quiz_start.html', context)
    elif request.session.get('quiz_status') == 'process':
        request.session['current_question'] += 1
        request.session['quiz_status'] = 'process'
        context = {'quiz.question': quiz.questions[request.session['current_question']],}
        return render(request, 'quiz/quiz.html', context)
    else:
        request.session['quiz_status'] = None
        request.session['current_question'] = 0
        context = {'result':'RESULT of quiz'}
        return render(request, 'quiz/quiz_finish.html', context)

    context = {'quiz': quiz, 'test': 'TEST'}
    return render(request, 'quiz/quiz.html', context)


def useful_links(request):
    context = {'var': 'quiz LINKS', }
    return render(request, 'quiz/useful_links.html', context)
