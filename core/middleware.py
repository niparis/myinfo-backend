"""
    Centralizing exception handling to send consistent error codes to the clients 
"""

import logging

from pydantic import ValidationError
import requests
from requests.exceptions import HTTPError

from django.http.response import JsonResponse
from django.middleware.common import MiddlewareMixin

from myinfo.responses import GenericErrorResponse

logger = logging.getLogger(__name__)

class ErrorMiddleware(MiddlewareMixin):


    def process_exception(self, request, exception):
        logger.warning(f"Middleware has caught an exception. exception={str(exception)}")

        if type(exception) in (ConnectionError, requests.exceptions.ConnectionError):
            resp = GenericErrorResponse(msg='Could not connect to a 3rd party API, please retry in a few minutes', details=str(exception))
            status = 503
        elif type(exception) in (HTTPError, ValueError):
            resp = GenericErrorResponse(msg='Internal Server Error')
            status = 500            
        elif type(exception) in (ValidationError,):
            resp = GenericErrorResponse(msg='Validation Error', details=str(exception))
            status = 400
        else:
            resp = GenericErrorResponse(msg="")
            status = 500
            logger.critical(f"exception of type {type(exception)} is not covered, go add it in code")

        return JsonResponse(resp.dict(), status=status)


         