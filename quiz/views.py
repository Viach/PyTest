from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import datetime, timedelta

from .models import Quiz, CategoryQuestion, UsefulLinks, Question


def index(request):
    categories = CategoryQuestion.objects.all()
    categories.length = len(categories)
    number_questions = categories.length * settings.NUMBER_QUESTIONS_PER_CATEGORY
    for k, v in enumerate(categories):
        categories[k].number_questions = len(Question.objects.all().filter(enabled=True).filter(category=v.id))
    context = {'categories': categories,
               'number_questions': number_questions,
               'time_quiz': (settings.TIME_PER_QUESTION * number_questions) // 60,
               'number_questions_in_blitz': settings.NUMBER_QUESTIONS_IN_BLITZ,
               'time_quiz_blitz': (settings.TIME_PER_QUESTION_BLITZ * settings.NUMBER_QUESTIONS_IN_BLITZ) // 60,
               }
    return render(request, 'quiz/index.html', context)


def quiz_start(request):
    blitz = True if request._get_post().get('blitz') == 'True' else False
    request.session['quiz'] = Quiz(blitz=blitz)
    request.session['time_per_question'] = settings.TIME_PER_QUESTION_BLITZ if blitz else settings.TIME_PER_QUESTION
    request.session['next_question'] = 0
    request.session['total_number_questions_in_quiz'] = len(request.session['quiz'].questions)
    for i in range(request.session['total_number_questions_in_quiz']):  # question index base - 0 !
        request.session[i] = {0, }

    return redirect('quiz_process')


def quiz_process(request):
    current_number_question = request.session.get('next_question', None)
    if current_number_question == None:
        return redirect('quiz_start')

    if current_number_question > 0:
        request.session[current_number_question - 1] = set(
            int(i) for i in dict(request._get_post()).get('user_answer', [0, ]))
    quiz_canceled = dict(request._get_post()).get('quiz_cancel', False)
    if current_number_question > len(request.session['quiz'].questions) - 1 or quiz_canceled:
        if quiz_canceled: request.session['next_question'] -= 1
        request.session['quiz_finished'] = True
        return redirect('quiz_finish')
    else:
        request.session['next_question'] += 1
        current_question = request.session['quiz'].questions[current_number_question]
        current_question.list_answers = current_question.get_answers()
        current_question.input_type = current_question.get_input_type()
        context = {'current_question': current_question,
                   'current_question_number_in_quiz': current_number_question + 1,
                   'number_questions': len(request.session['quiz'].questions),
                   }
        return render(request, 'quiz/quiz_process.html', context)


def quiz_finish(request):
    if not request.session.get('quiz_finished', False):
        return redirect('quiz_start')

    request.session['quiz'].stop_time = datetime.now()
    request.session['quiz'].time_delta = request.session['quiz'].stop_time - request.session[
        'quiz'].start_time - timedelta(
        seconds=2)  # correction for time delay  with js-contdown in template
    list_result = []
    for k in range(request.session['total_number_questions_in_quiz']):
        r = request.session['quiz'].questions[k].get_correct_answer() == request.session[k]
        list_result.append(r)
        request.session['quiz'].questions[k].answered += 1
        if not r: request.session['quiz'].questions[k].wrong_answered += 1
        request.session['quiz'].questions[k].save()

    c_a = list_result.count(True)  # correct answers
    w_a = list_result.count(False)  # wrong answers
    n_a = c_a + w_a
    k = round(c_a / n_a * 100)
    data_result = [c_a, w_a, n_a, k, k >= 80]
    result = [list_result, data_result]

    context = {'result': result,
               'questions_answers': [
                   [r,
                    a.name,
                    a.code,
                    a.get_answers(),
                    [x[1] for x in a.get_answers() if x[0] in a.get_correct_answer()],
                    #                    [dict(a.list_answers)[i] for i in a.get_correct_answer()],
                    a.user_answer,
                    a.explanation]
                   for r, a in
                   zip(result[0], request.session['quiz'].questions[:request.session['next_question']])],
               'quiz_time': request.session['quiz'].time_delta.__str__().split('.')[0],
               }
    del request.session['next_question']
    del request.session['quiz']
    del request.session['quiz_finished']
    return render(request, 'quiz/quiz_finish.html', context)


def useful_links(request):
    context = {'links': UsefulLinks.objects.all(), }
    return render(request, 'quiz/useful_links.html', context)


def contact(request):
    r = request._get_post()
    if len(r) and r['ban_spam'] == '6':  # email is not empty and should be send
        request.session['mail'] = EmailMessage(
            r['mail_subject'],
            r['mail_body'],
            'from@pytest.debos.net',
            ['vch@localhost', ],
            reply_to=['another@example.com'],
            # headers={'Message-ID': 'foo'},
        )
        request.session['mail'].send(fail_silently=False)
        del request.session['mail']
        return redirect('index')
    request.session['mail'] = {'subject': 'Вітаю... тут пишемо заголовок повідомлення',
                               'body': 'А тут текст листа...', }
    context = {'mail': request.session['mail'], }
    return render(request, 'quiz/contact.html', context)


def error_500(request):
    context = {'error': 'ERROR: 500'}
    return render(request, 'quiz/error.html', context)


def error_404(request):
    context = {'error': 'ERROR: 404'}
    return render(request, 'quiz/error.html', context)
