from django.test import TestCase
from unittest.mock import MagicMock, patch

import json

from myinfo.service import authorize_url
from myinfo.entities import Person
from myinfo.responses import PersonResponse
from libs.myinfo_client.client import MyInfoClient


def load_person_data():
    with open('myinfo/tests_data/person.json', 'r') as fin:
        return json.loads(fin.read())


class MyInfoService(TestCase):

    def test_authorize_url(self):
        """Testing that the authorize url is correctly created"""
        url = authorize_url(state='i-am-test')
        expected_url = 'https://test.api.myinfo.gov.sg/com/v3/authorise?client_id=STG2-MYINFO-SELF-TEST&attributes=uinfin,name,sex,race,nationality,dob,email,mobileno,regadd,housingtype,hdbtype,marital,edulevel,noa-basic,ownerprivate,cpfcontributions,cpfbalances&purpose=credit%20risk%20assessment&state=i-am-test&redirect_uri=http://localhost:3001/callback'
        self.assertEqual(url, expected_url)

    def test_person_can_be_created(self):
        """Testing that our person entity is created without errors from fixture data"""
        data = load_person_data()
        Person(**data)

    def test_person_response_can_be_created(self):
        data = load_person_data()
        person = Person(**data)
        content = PersonResponse(msg="successfully retrieved a person", data=person)




