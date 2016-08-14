from django.shortcuts import render, HttpResponse
import os
from path import Path
from file.models import Document
from course.models import Course
from django.core.files import File
from django.conf import settings


def presentation(request):
    return render(request, 'projector/presentation.html')


def convert_to_slide(request, **kwargs):    # add the choice of theme or not
    #gives the full path to the file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path_base_dir = Path(base_dir)
    path_to_rst_file = path_base_dir.joinpath('media/{}/{}'.format(kwargs.get('course_code'), kwargs.get('file_name')))
    path_to_theme= path_base_dir.joinpath('media/avalanche')
    if path_to_rst_file.exists() and Path(kwargs.get('file_name')).ext == '.rst':
        os.system("landslide {} -m -i -d {}/media/{}/{}.html -t {}".format(path_to_rst_file, base_dir, kwargs.get('course_code'), kwargs.get('file_name').split('.')[0], path_to_theme))
        try:
            filename = kwargs.get('file_name').split('.')[0]+'.html'
            Document.objects.get(file_name=filename)
            raise Exception('File name already exists')
        except Document.DoesNotExist:
            file_path = Path('media/{}/{}'.format(kwargs.get('course_code'), filename))
            course = Course.objects.get(course_code=kwargs.get('course_code'))
            with open(file_path) as f:
                file_obj = File(f)
                doc = Document.objects.create(file_name=filename, course=course, size=file_obj.size)
                #filename = filename.split('.')[0]+'.rst'
                #doc_rst = Document.objects.get(file_name=filename)
                doc.document = file_path.split('media/')[1]    # one can use Path to select sub path later
                doc.file_type = 'NOTES'
                doc.save()
    else:
        return HttpResponse('HTML slide not created. Please make sure the file exists or has extension .rst')

    filename = kwargs.get('file_name').split('.')[0]+'.rst'
    course_code = kwargs.get('course_code')
    file_path = Document.objects.get(file_name=filename, document='{}/{}'.format(course_code, filename))
    os.remove(settings.MEDIA_ROOT+'{}'.format(file_path.document))
    file_path.delete()

    return HttpResponse('HTML slide created successfully')



