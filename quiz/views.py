from django.shortcuts import render, redirect
from .models import Quiz, G

g = G()  # my global variable


def index(request):
    context = {'var': 'quiz index.html', }
    return render(request, 'quiz/index.html', context)


def quiz(request, *args):
    status = args[0]
    if status == 'start':
        request.session['current_question'] = -1
        g.quiz = Quiz()
        context = {'info': "INFO about quiz"}
        return render(request, 'quiz/quiz_start.html', context)
    elif status == 'next':
        request.session['current_question'] += 1
        if request.session['current_question'] > len(g.quiz.questions) - 1:
            return redirect('quiz', 'finish' )
        else:
            context = {'current_question': g.quiz.questions[request.session['current_question']],
                       'current_question_number_in_quiz': request.session['current_question'],
                       'info': 'Quiz in process...',
                       }
            return render(request, 'quiz/quiz.html', context)
    elif status == 'finish':
        request.session['current_question'] = 0
        context = {'result': 'RESULT of quiz',}
        return render(request, 'quiz/quiz_finish.html', context)
    else:
        context = {'info': 'ERROR', }
        return render(request, 'quiz/quiz.html', context)


def useful_links(request):
    context = {'var': 'quiz LINKS', }
    return render(request, 'quiz/useful_links.html', context)
