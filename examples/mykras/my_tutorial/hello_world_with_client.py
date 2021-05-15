from prefect import task
from prefect import Client

@task
def say_hello():
    print('Hello, world!')

from prefect import Flow

with Flow('hello_worlds_with_client') as flow:
    say_hello()

state = flow.run()

client = Client()
client.create_project(project_name='hello_worlds_with_client.py')

flow.register(project_name='hello_worlds_with_client.py')
flow.run()
