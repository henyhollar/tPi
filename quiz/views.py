# Create your views here.

import os
from path import Path
from course.models import Course
from django.core.files import File
from .models import Questions, Results
import json

from rest_framework.views import APIView
from django.shortcuts import render, HttpResponse



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
            print topic
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
    """

    def get(self, request):
        #mark = Results.objects.get(user=request.user).mark_obtained
        pass

    def post(self, request, **kwargs):
        mark = 0
        res = Results.objects.create(user=request.user, submission=request.data.get('submission'))
        #for id,answers in json.loads(request.data.get('submission')).items()
            #real_answers = Questions.objects.get(id=id).answers
            #if cmp(real_answers,answers) == 0:
                #mark+=1
        res.mark_obtained = mark
        res.save()