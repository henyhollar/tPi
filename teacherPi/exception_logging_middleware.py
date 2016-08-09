import logging
from django.http import HttpResponse
from file.models import SlideConverterError


class ExceptionLoggingMiddleware(object):
    def process_exception(self, request, exception):
        if not isinstance(exception, SlideConverterError):
            logging.exception('Exception handling request for ' + request.path)
        return HttpResponse('File name already exists in the db. '
                                 'This might be due to double clicking the slide converter')