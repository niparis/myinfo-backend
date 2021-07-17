import logging

from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest

import pydantic


from myinfo.service import get_person_data, authorize_url
from myinfo.responses import GenericResponse, GenericErrorResponse, PersonResponse
from myinfo.requests import GetPersonData

from libs.validation.decorators import validate_get
# Create your views here.

logger = logging.getLogger(__name__)

def authorise_url(request):
    
    try:
        # we call the service method
        url = authorize_url()    
    except ConnectionError:
        raise ConnectionError('Myinfo seems to be busy, please retry later')

    content = GenericResponse(
        msg='Here is an authorization url',
        data= url
    )

    return JsonResponse(content.dict())


# we validate the request. The validated object is passed as "data" to the view function
@validate_get(GetPersonData)
def person_data(request, data: GetPersonData):
    # this is our controller. It is intended to only take care of the HTTP layer
    
    try:
        # we call the service method, which abstract all the business logic for 
        person = get_person_data(code=data.code[0])    
    except pydantic.ValidationError:
        # appropriate final exceptions are raise. The exceptions middleware will dispatch them, returning the actual HTTP responses.
        raise ValueError('Unable to validate the person object we got from myinfo')
    except ConnectionError:
        raise ConnectionError('Error connecting to MyInfo. Please retry in a few minutes')

    # The response object is built, based on a class. It is validated at runtime, so that the clients will never get anything unexpected.
    content = PersonResponse(msg="successfully retrieved a person", data=person)
    return JsonResponse(content.dict())






