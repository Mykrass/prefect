#https://colab.research.google.com/drive/10bb6eUXanlavZbr6GoAMtfO_00NZKmrP

# prefect backend server
# prefect agent local start
# prefect server start

import random
from datetime import datetime, timedelta

from prefect import Flow, task
from prefect.schedules import IntervalSchedule

from prefect import Client


@task
def extract():
    return [1, 2, 3]


@task
def transform(x):
    return [i * 10 for i in x]


@task
def load(y):
    print("Received y: {}".format(y))

schedule = IntervalSchedule(
    start_date=datetime.utcnow(),
    interval=timedelta(minutes=1),
    end_date=datetime.utcnow() + timedelta(minutes=10),
)

with Flow("ETL",  schedule=schedule) as flow:
    e = extract()
    t = transform(e)
    l = load(t)

state = flow.run()

client = Client()
client.create_project(project_name='mykras_hello_client')

flow.register(project_name='mykras_hello_client')
# %paste