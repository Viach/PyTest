from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from datetime import datetime, timedelta

from .models import Quiz, CategoryQuestion, UsefulLinks, Question



def index(request):
    categories = CategoryQuestion.objects.all()
    categories.length = len(categories)
    for k, v in enumerate(categories):
        categories[k].number_questions = len(Question.objects.all().filter(enabled=True).filter(category=v.id))
    context = {'categories': categories, }
    return render(request, 'quiz/index.html', context)


def quiz_start(request):

    request.session['quiz'] = Quiz()
    context = {'number_questions': len(request.session['quiz'].questions)}
    return render(request, 'quiz/quiz_start.html', context)


def quiz_process(request):
    if request.session['quiz'].current_number_question >= 0:  # write user answer for previous  question
        request.session['quiz'].questions[request.session['quiz'].current_number_question].user_answer = set(
            int(i) for i in dict(request._get_post()).get('user_answer', [0, ]))
    n_q =  request._get_post().get('next_question')
    request.session['quiz'].current_number_question = int(n_q) if n_q else 0

    if request.session['quiz'].current_number_question > len(request.session['quiz'].questions) - 1:
        return redirect('quiz_finish')
    else:
        current_question = request.session['quiz'].questions[request.session['quiz'].current_number_question]
        current_question.list_answers = current_question.get_answers()
        current_question.input_type = current_question.get_input_type()
        context = {'current_question': current_question,
                   'current_question_number_in_quiz': request.session['quiz'].current_number_question + 1,
                   'number_questions': len(request.session['quiz'].questions),
                   }
        return render(request, 'quiz/quiz_process.html', context)


def quiz_finish(request):
    #if 'quiz' not in request.session['quiz'].__dict__.keys():        return redirect('quiz_start')
    request.session['quiz'].stop_time = datetime.now()
    request.session['quiz'].time_delta = request.session['quiz'].stop_time - request.session['quiz'].start_time - timedelta(
        seconds=2)  # correction for time delay  with js-contdown in template
    result = request.session['quiz'].result()
    result[0] = result[0][:request.session['quiz'].current_number_question]
    context = {'result': result,
               'questions_answers': [
                   [r,
                    a.name,
                    a.code,
                    [dict(a.list_answers)[i] for i in a.get_correct_answer()],
                    a.user_answer,
                    a.explanation]
                   for r, a in zip(result[0], request.session['quiz'].questions[:request.session['quiz'].current_number_question])],
               'quiz_time': request.session['quiz'].time_delta.__str__().split('.')[0],
               }
    request.session['quiz'].current_number_question = 0
    del s
    return render(request, 'quiz/quiz_finish.html', context)


def useful_links(request):
    context = {'links': UsefulLinks.objectrequest.session['quiz'].all(), }
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
        request.session['quiz'].mail.send(fail_silently=False)
        del request.session['mail']
        return redirect('index')
    request.session['mail'] = {'subject': 'Вітаю... тут пишемо заголовок повідомлення', 'body': 'А тут текст листа...', }
    context = {'mail': request.session['mail'], }
    return render(request, 'quiz/contact.html', context)
