from django.shortcuts import render


def index(request):
    context = {'var': 'quiz index.html', }
    return render(request, 'quiz/index.html', context)


def quiz(request):
    context = {'var': 'quiz QUIZ', }
    return render(request, 'quiz/quiz.html', context)

def useful_links(request):
    context = {'var': 'quiz LINKS', }
    return render(request, 'quiz/useful_links.html', context)
