from dask_flow import airflow

from prefect.engine.executors import DaskExecutor

executor = DaskExecutor(address = '10.255.253.2:8786')

flow.run(executor=executor)