from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from datetime import datetime, timedelta

from .models import Quiz, S, CategoryQuestion, UsefulLinks, Question

s = S()  # my session


def index(request):
    categories = CategoryQuestion.objects.all()
    categories.length = len(categories)
    for k, v in enumerate(categories):
        categories[k].number_questions = len(Question.objects.all().filter(enabled=True).filter(category=v.id))
    context = {'categories': categories, }
    return render(request, 'quiz/index.html', context)


def quiz(request, *args):
    status = args[0]
    if status == 'start':
        s.quiz = Quiz()
        s.quiz.current_number_question = -1
        s.quiz.start_time = datetime.now()
        context = {'number_questions': len(s.quiz.questions)}
        return render(request, 'quiz/quiz_start.html', context)
    elif status == 'next':
        print(s.__dict__.keys())
        if 'quiz' not in s.__dict__.keys():
            return redirect('quiz', 'start')
        if s.quiz.current_number_question >= 0:
            s.quiz.questions[s.quiz.current_number_question].user_answer = set(
                int(i) for i in dict(request._get_post()).get('user_answer', [0, ]))

        s.quiz.current_number_question += 1
        if s.quiz.current_number_question > len(s.quiz.questions) - 1:
            return redirect('quiz', 'finish')
        else:
            current_question = s.quiz.questions[s.quiz.current_number_question]
            current_question.list_answers = current_question.get_answers()
            current_question.input_type = current_question.get_input_type()
            context = {'current_question': current_question,
                       'current_question_number_in_quiz': s.quiz.current_number_question + 1,
                       'number_questions': len(s.quiz.questions),
                       }
            return render(request, 'quiz/quiz.html', context)
    elif status == 'finish':
        if 'quiz' not in s.__dict__.keys():
            return redirect('quiz', 'start')
        s.quiz.stop_time = datetime.now()
        s.quiz.time_delta = s.quiz.stop_time - s.quiz.start_time - timedelta(
            seconds=2)  # correction for time delay  with js-contdown in template
        result = s.quiz.result()
        result[0] = result[0][:s.quiz.current_number_question]
        context = {'result': result,
                   'questions_answers': [
                       [r,
                        a.name,
                        a.code,
                        [dict(a.list_answers)[i] for i in a.get_correct_answer()],
                        a.user_answer,
                        a.explanation]
                       for r, a in zip(result[0], s.quiz.questions[:s.quiz.current_number_question])],
                   'quiz_time': s.quiz.time_delta.__str__().split('.')[0],
                   }
        s.quiz.current_number_question = 0
        del s.quiz
        return render(request, 'quiz/quiz_finish.html', context)
    else:
        context = {'info': 'ERROR', }
        return render(request, 'quiz/quiz.html', context)


def useful_links(request):
    context = {'links': UsefulLinks.objects.all(), }
    return render(request, 'quiz/useful_links.html', context)


def contact(request):
    r = request._get_post()
    if len(r) and r['ban_spam'] == '6':  # email is not empty and should be send
        s.mail = EmailMessage(
            r['mail_subject'],
            r['mail_body'],
            'from@pytest.debos.net',
            ['vch@localhost', ],
            reply_to=['another@example.com'],
            # headers={'Message-ID': 'foo'},
        )
        s.mail.send(fail_silently=False)
        del s.mail
        return redirect('index')
    s.mail = {'subject': 'Вітаю... тут пишемо заголовок повідомлення', 'body': 'А тут текст листа...', }
    context = {'mail': s.mail, }
    return render(request, 'quiz/contact.html', context)
