from django.shortcuts import render, HttpResponse
import os
from path import Path


def presentation(request):
    return render(request, 'projector/presentation.html')


def convert_to_slide(request, **kwargs):
    #gives the full path to the file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path_base_dir = Path(base_dir)
    path_to_rst_file = path_base_dir.joinpath('media\{}\{}.rst'.format(kwargs.get('course_code'), kwargs.get('file_name')))
    print path_to_rst_file
    if path_to_rst_file.exists():
        os.system("landslide {} -i -d {}/media/presentation.html".format(path_to_rst_file, base_dir))
    else:
        return HttpResponse('HTML slide not created. Please make sure the file exists or has extension .rst')

    return HttpResponse('HTML slide created successfully')



