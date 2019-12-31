from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from datetime import datetime

def my_func(**kwargs):
        print(kwargs)
        return kwargs['param_1']

with DAG('python_dag', description='Python DAG', schedule_interval='*/5 * * * *', start_date=datetime(2018, 11, 1), catchup=False) as dag:
        dummy_task      = DummyOperator(task_id='dummy_task', retries=3)
        python_task     = PythonOperator(task_id='python_task', python_callable=my_func, op_kwargs={'param_1': 'one', 'param_2': 'two', 'param_3': 'three'})

        dummy_task >> python_task