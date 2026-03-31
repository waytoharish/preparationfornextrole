from airflow import DAG
from airflow.decorators import task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime
import json

with DAG(
    dag_id="parent_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    @task
    def read_json():
        # Example JSON (replace with S3/file read)
        data = {
            "tables": ["table1", "table2", "table3"]
        }
        return data["tables"]

    tables = read_json()

    trigger_child = TriggerDagRunOperator.partial(
        task_id="trigger_child_dag",
        trigger_dag_id="child_dag",
        wait_for_completion=False,  # optional
    ).expand(
        conf=tables.map(lambda t: {"table_name": t})
    )
