from django.shortcuts import render
from .models import Quiz

quiz = Quiz()


def index(request):
    context = {'var': 'quiz index.html', }
    return render(request, 'quiz/index.html', context)


def quiz(request,*args):
    status = args[0]
    if status == 'start':
        request.session['current_question'] = 0
        context = {'info':"INFO about quiz"}
        return render(request, 'quiz/quiz_start.html', context)
    elif int(status) in range(100):

        context = {'quiz.question': quiz.questions[int(status)+1],}
        return render(request, 'quiz/quiz.html', context)
    else:
        request.session['current_question'] = 0
        context = {'result':'RESULT of quiz'}
        return render(request, 'quiz/quiz_finish.html', context)

    context = {'quiz': quiz, 'test': 'TEST'}
    return render(request, 'quiz/quiz.html', context)


def useful_links(request):
    context = {'var': 'quiz LINKS', }
    return render(request, 'quiz/useful_links.html', context)
