## How To Start ?

### Requirements

1. Need rabbit mq server to be installed. 
2. Create a virtual environment with ```python3 -m venv env```
3. Activate environment
4. run ```pip install -r requirements.txt```
5. run ```python manage.py migrate*```
6. run ```python manage.py runserver```


- To start celery worker run below command

```
celery -A tech_test worker --loglevel=INFO
```