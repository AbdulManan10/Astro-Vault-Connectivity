from airflow import DAG
from airflow.hooks.base import BaseHook
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from datetime import datetime




def print_var():
    my_var = Variable.get("StockX_user")
    print(f'user: {my_var}')

    my_var2 = Variable.get("StockX_pass")
    print(f'password: {my_var2}')


with DAG('StockX_FTP_Key_Management', start_date=datetime(2022, 1, 1), schedule_interval=None) as dag:
    test_task = PythonOperator(task_id='test-task',python_callable=print_var,)