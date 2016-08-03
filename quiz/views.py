# Create your views here.

import os
from path import Path
from course.models import Course
from django.core.files import File
from .models import Questions, Results
import json

from rest_framework.views import APIView
from django.shortcuts import render, HttpResponse
from rest_framework.response import Response

import random


def upload_quiz(request, **kwargs):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path_base_dir = Path(base_dir)
    path_to_rst_file = path_base_dir.joinpath('media/{}/{}'.format(kwargs.get('course_code'), kwargs.get('file_name')))
    if path_to_rst_file.exists() and Path(kwargs.get('file_name')).ext == '.rst':
        file_path = Path('media/{}/{}'.format(kwargs.get('course_code'), kwargs.get('file_name')))
        course = Course.objects.get(course_code=kwargs.get('course_code'))
        with open(file_path) as f:
            file_obj = File(f)
            file_line_list = file_obj.readlines()
            str_list = filter(bool, file_line_list)
            topic = [line.strip('#').strip() for i, line in enumerate(str_list) if (line.strip('\n').startswith('#') or line.strip('\r\n').startswith('#'))]
            topic = ' '.join(topic)
            marker_index = [i for i, line in enumerate(str_list) if (line.strip('\n').startswith('--') or line.strip('\r\n').startswith('--'))]
            for i in xrange(len(marker_index)):
                answer = {}
                question = []
                try:
                    items = str_list[marker_index[i]+1:marker_index[i+1]]
                    for item in items:
                        if item.strip().startswith('-'):
                            ans = item.strip('-').strip().split(':')

                            if ans[1].upper() == 'T':
                                ans[1] = True
                            elif ans[1].upper() == 'F':
                                ans[1] = False
                            else:
                                pass

                            answer.update(dict([tuple(ans)]))
                            print answer
                        else:
                            question.append(item.strip())
                            print question

                    if answer.values().count(True) == 0:
                        question_type = 0
                    elif answer.values().count(True) == 1:
                        question_type = 1
                    else:
                        question_type = 2

                    print question_type
                    quest = Questions.objects.create(course=course, topic=topic, question=question,
                                                     question_type=question_type, answer=answer)
                    quest.save()
                except IndexError:
                    items = str_list[marker_index[i]+1:]
                    for item in items:
                        if item.strip().startswith('-'):
                            ans = item.strip('-').strip().split(':')

                            if ans[1].upper() == 'T':
                                ans[1] = True
                            elif ans[1].upper() == 'F':
                                ans[1] = False
                            else:
                                pass

                            answer.update(dict([tuple(ans)]))
                            print answer
                        else:
                            question.append(item.strip())
                            print question

                    if answer.values().count(True) == 0:
                        question_type = 0
                    elif answer.values().count(True) == 1:
                        question_type = 1
                    else:
                        question_type = 2

                    print question_type
                    quest = Questions.objects.create(course=course, topic=topic, question=question,
                                                     question_type=question_type, answer=answer)
                    quest.save()

    else:
        return HttpResponse('Quiz not uploaded successfully. Please make sure the file exists or has extension .rst')

    return HttpResponse('Quiz uploaded successfully')


# use html tag to import images for multi-part questions
# use dictionary cmp for marking view

class SubmitQuiz(APIView):
    """
    Parameter for post:
        submission: JSON of question_ids and associated answers dictionary

    Save the json from the front-end like so:
        {'id':{'option_1':True,'option_2':True}} and
        {'id': {'Gap': 'x^2'}} for fill in the gap type question
        and return a list of them all at once
    """

    def get(self, request):  # code to return stat for the student will be called automatically after submission
        result = Results.objects.filter(user=request.user)  # pass to a stat function

    def post(self, request, **kwargs):
        mark = 0
        res = Results.objects.create(user=request.user, submission=request.data.get('submission'))
        list_of_submission = json.loads(request.data.get('submission'))
        for element in list_of_submission:
            for pk, submitted_answers in element.items():
                res.question = pk
                real_answers = Questions.objects.get(id=pk).answers
                if cmp(real_answers, submitted_answers) == 0:
                    mark += 1
        res.mark_obtained = mark

        res.save()

        return Response('Your score is: {}. Please check your statistics'.format(mark))


def take_quiz(request, **kwargs):
    # supply with topic and course and the no of questions needed
    # generate the list of ids of questions and shuffle
    #return a sliced list (with no_of_questions) of the list above

    course = kwargs.get('course')
    topic = kwargs.get('topic')
    no_of_questions = kwargs.get('no_of_questions')

    list_of_question_ids = Questions.objects.filter(course=course, topic=topic).values_list('pk', flat=True)

    random.shuffle(list_of_question_ids)
    shuffled_list_of_questions = list_of_question_ids[:(no_of_questions-1)]

    return HttpResponse(Questions.objects.filter(pk__in=shuffled_list_of_questions))


def topic(request, **kwargs):
    # supply with course name
    course = kwargs.get('course')

    list_of_topics = Questions.objects.filter(course=course).values_list('topic', flat=True)

    list_of_topics = set(list_of_topics)

    return HttpResponse(list_of_topics)


def stats(request, **kwargs):
    student = kwargs.get('student')
    # calls the statistics function written in pandas