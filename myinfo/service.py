"""
    This is the service layer.
    It contains the business logic specific to our service.
    It is not exposed to the HTTP layer of our service, so that it can purely focus on the business logic.
    Here i've opted to keep the code to interact with MyInfo in a separate library - it made code reuse easier.
    In a real life scenario, that code could be integrated in the service. 
    The decision would depend on wether we'd expect to reuse that library in other services.
"""
import logging

from pydantic import ValidationError


from libs.myinfo_client.client import MyInfoClient
from libs.myinfo_client.security import get_decoded_access_token, get_decrypted_person_data


from myinfo.entities import Person


logger = logging.getLogger(__name__)

def authorize_url(state: str="blahblah") -> str:
    client = MyInfoClient()
    return client.get_authorise_url(state=state)   
    

def get_person_data(code: str) -> Person:
    return _get_person_data(client=MyInfoClient(), code=code)

def _get_person_data(client: MyInfoClient, code: str) -> Person:
    # Getting access token with code
    try:
        resp = client.get_access_token(code)
    except ConnectionError as ex:
        logger.exception('Connection error when calling get_person')
        raise ex

    logger.info('got access token')
    access_token = resp["access_token"]

    # Decoding access token
    decoded_access_token = get_decoded_access_token(access_token)
    uinfin = decoded_access_token["sub"]

    # Getting person data
    try:
        resp = client.get_person(uinfin=uinfin, access_token=access_token)
    except ConnectionError as ex:
        logger.exception('Connection error when calling get_person')
        raise ex

    import json
    with open('client_get_person_response.json', 'w') as fin:
        fin.write(json.dumps(resp))

    decrypted = get_decrypted_person_data(resp)
    logger.info('person data decrypted')

    try:
        person  = Person(**decrypted)
    except ValidationError:
        logger.exception('We were not able to decode the person. Going to log the raw object for easier debugging')
        logger.error(decrypted)
        raise ValidationError('unable to decode the person')
    

    return person
