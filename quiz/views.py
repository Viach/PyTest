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
        if 'quiz' not in g.__dict__.keys():
            return redirect('quiz', 'start')
        if request.session['current_question'] >= 0:
            g.quiz.questions[request.session['current_question']].user_answer = set(
                int(i) for i in dict(request._get_post()).get('user_answer', [0, ]))

        request.session['current_question'] += 1
        if request.session['current_question'] > len(g.quiz.questions) - 1:
            return redirect('quiz', 'finish')
        else:
            current_question = g.quiz.questions[request.session['current_question']]
            current_question.list_answers = current_question.get_answers()
            current_question.input_type = current_question.get_input_type()
            context = {'current_question': current_question,
                       'current_question_number_in_quiz': request.session['current_question'] + 1,
                       'info': 'Quiz in process...',
                       }
            return render(request, 'quiz/quiz.html', context)
    elif status == 'finish':
        request.session['current_question'] = 0
        result = g.quiz.result()
        context = {'result': result,
                   'answer_r_n_c_u_e': [  # r_c_u_e -> result, question_name, correct, user, explanation
                                      [r,
                                       a.name,
                                       a.get_correct_answer(),
                                       a.user_answer,
                                       a.explanation]
                                      for r, a in zip(result, g.quiz.questions)],
                   }
        return render(request, 'quiz/quiz_finish.html', context)
    else:
        context = {'info': 'ERROR', }
        return render(request, 'quiz/quiz.html', context)


def useful_links(request):
    context = {'var': 'quiz LINKS', }
    return render(request, 'quiz/useful_links.html', context)
