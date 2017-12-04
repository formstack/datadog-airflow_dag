from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2017, 11, 22),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

tutorial_dag = DAG(
    dag_id='tutorial',
    default_args=default_args,
    schedule_interval='0 0 * * *',
    dagrun_timeout=timedelta(hours=1)
)

task_one = BashOperator(task_id='print_date', bash_command='date', dag=tutorial_dag)
task_two = BashOperator(task_id='sleep', bash_command='sleep 5', retries=3, dag=tutorial_dag)

command_template = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7) }}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

task_three = BashOperator(
    task_id='templated_task',
    bash_command=command_template,
    params={'my_param': 'Dag, yo'},
    dag=tutorial_dag
)

task_two.set_upstream(task_one)
task_three.set_upstream(task_one)
