from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context = {'var': 'quiz index.html', }
    return render(request, 'quiz/index.html', context)


def quiz(request):
    return HttpResponse("Start test here.")


def useful_links(request):
    return HttpResponse("Useful linkks  here.")
