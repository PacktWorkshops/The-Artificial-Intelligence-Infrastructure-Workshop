# change workding dir
cd Activity01/

# copy dag to airflow HOME dir
cp ./ratio_dag.py ~/airflow/dags/

# launch airflow
airflow webserver -p 8080
airflow scheduler

# check dag
airflow list_dags

# trigger dag
airflow trigger_dag -c '
{
    "path_vids": "../Data/USvideos.csv.zip",
    "path_cats": "../Data/US_category_id.json",
    "date": "17.14.11",
    "path_output": "../Data/Ratio_Likes_Dislikes.csv"
}' 'ratio_dag'
