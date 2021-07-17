"""
    A reusable library to validate requests.
"""

import logging
from django.http import JsonResponse
import pydantic

from myinfo.responses import GenericErrorResponse
# Create your views here.

logger = logging.getLogger(__name__)


def parameterized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer

@parameterized
def validate_get(f, request_class):

    def requestchecker(request, *args):
        print(request.GET)
        try:
            data = request_class(**request.GET)
        except pydantic.ValidationError as ex:
            logger.exception(f'Validation error for {request_class}')
            resp = GenericErrorResponse(msg=f"can't process this request\n {str(ex)}")
            return JsonResponse(resp.dict(), status=400)
        return f(request, data, *args)

    return requestchecker

