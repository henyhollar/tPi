from django.shortcuts import render, HttpResponse
import os
from path import Path


def presentation(request):
    return render(request, 'projector/presentation.html')


def convert_to_html(request):
    #gives the full path to the file
    path_to_rst_file = Path(request.data['path'])
    if path_to_rst_file.isfile() and path_to_rst_file.ext == '.rst':
        os.system("landslide {} -i -d {}/media/presentation.html".format(request.data['path'], os.path.dirname(os.path.abspath(__file__))))

    return HttpResponse('HTML created successfully')



