from django.shortcuts import render, HttpResponse
import os
from path import Path
from file.models import Document
from course.models import Course
from django.core.files import File


def presentation(request):
    return render(request, 'projector/presentation.html')


def convert_to_slide(request, **kwargs):
    #gives the full path to the file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path_base_dir = Path(base_dir)
    path_to_rst_file = path_base_dir.joinpath('media/{}/{}'.format(kwargs.get('course_code'), kwargs.get('file_name')))
    if path_to_rst_file.exists() and Path(kwargs.get('file_name')).ext == '.rst':
        os.system("landslide {} -i -d {}/media/{}/{}.html".format(path_to_rst_file, base_dir, kwargs.get('course_code'), kwargs.get('file_name').split('.')[0]))
        try:
            filename = kwargs.get('file_name').split('.')[0]+'.html'
            Document.objects.get(file_name=filename)
            raise Exception('File name already exists')
        except Document.DoesNotExist:
            file_path = Path('media/{}/{}'.format(kwargs.get('course_code'), filename))
            print file_path
            course = Course.objects.get(course_code=kwargs.get('course_code'))
            with open(file_path) as f:
                file_obj = File(f)
                doc = Document.objects.create(file_name=filename, course=course, size=file_obj.size)
                doc.save()
    else:
        return HttpResponse('HTML slide not created. Please make sure the file exists or has extension .rst')

    return HttpResponse('HTML slide created successfully')



