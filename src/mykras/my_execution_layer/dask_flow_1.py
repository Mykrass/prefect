from dask_flow import flow

from prefect.engine.executors import DaskExecutor

executor = DaskExecutor(address = '127.0.0.1:8786')

flow.run(executor=executor)