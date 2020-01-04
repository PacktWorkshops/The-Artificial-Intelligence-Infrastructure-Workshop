# change workding dir
cd Exercise06

# launch airflow
airflow webserver -p 8080 &
airflow scheduler &

# copy dag to airflow HOME dir
cp ./top_cat_dag.py ~/airflow/dags/

# check dag
airflow list_dags

# trigger dag
airflow trigger_dag -c '
{
    "path_vids": "../Data/USvideos.csv.zip",
    "path_cats": "../Data/US_category_id.json",
    "date": "17.14.11",
    "path_output": "../Data/top_10_trendy_cats.csv"
}' 'top_cat_dag'
