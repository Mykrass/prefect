from prefect import task, Flow
import datetime
import random

@task
def inc(x):
    return x+1

@task
def dec(x):
    return  x-1

@task
def add(x, y):
    return x + y