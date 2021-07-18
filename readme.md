# MyInfo Backend

This is a MyInfo demo backend
It offers API endpoints to retrieve a person's data from Myinfo's test environment.

## How to run

### setup - option A - Poetry [recommended]

This requires having poetry install on your system, go [there](https://python-poetry.org/docs/) if you don't have it.

```
poetry install
poetry shell
python manage.py runserver 3001
```

### setup - option B - Classic

Create and activate your virtual environment with your tool of choice
then

```
pip install -r requirements.txt
python manage.py runserver 3001
```

### How to test

Some basic test cases are included.

To run: 

activate virtual environment

then

`python manage.py test`

## What can be done

First, run the Django API server (cf above, setup A or B)

### 1. Retrieve the MyInfo authorization URL
    
    - Either from the API, from 

    http://127.0.0.1:3001/myinfo/get-authorize-url/    


    - Or just copy paste from here as it's a static 

    https://test.api.myinfo.gov.sg/com/v3/authorise?client_id=STG2-MYINFO-SELF-TEST&attributes=uinfin,name,sex,race,nationality,dob,email,mobileno,regadd,housingtype,hdbtype,marital,edulevel,noa-basic,ownerprivate,cpfcontributions,cpfbalances&purpose=credit%20risk%20assessment&state=blahblah&redirect_uri=http://localhost:3001/callback

### 2. Visit the URL and follow the steps on the MyInfo API

### 3. Person Data will be returned as a JSON document
    After going through the MyInfo API, it will callback our backend.
    It will process the result and return it as part of a Json response.

# Design Choices

1. Everything is validated
    A. Each request and each response have a schema, 
    B. Business entities helps validate data created in the the services, or coming from third parties

2. Strict separation between:
    A. the HTTP controller (or view in Django) that purely takes care of the request/response validation, and of
    B. the service layer, responsible for the business logic. The HTTP and data layers are abstracted from it so that it can focus on the hardest part. It includes business entities         
    C. the data layer **not implemented as unnecessary** - would be strictly separated from the service layer and focused purely on the interation with the datastore.
3. Code that could be used in other services is offloaded to libraries (`libs` folder on top)
4. Central management of exceptions implemented as a middleware. Ensures consistency in the API's error responses.


Comments in the code give more color on the decision process.

## Next steps

Immediate next step, that i think are out of scope for such a test:

1. Dockerize the app (unnecessary in its current state. Starts to pay off once we have a Storage Backend)
2. Selenium test cases (seems like the ideal way to test the integration with MyInfo - right now the test cases are fairly primitive as they dont account for the behaviour of MyInfo)
3. Push the the communication with MyInfo to a queue (i've had pretty inconsitent response times, including a few timeouts)
4. CI/CD, including automatic code formating, security scans, unit tests, static code quality analysis
5. Configuration management, to have different environement. Would be implemented by environment variables.

