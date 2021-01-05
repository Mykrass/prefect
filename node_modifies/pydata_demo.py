from prefect import task, Flow


@task
def hello_world():
    print("Hello world!")


with Flow("my first flow") as f:
    r = hello_world()

f.run()