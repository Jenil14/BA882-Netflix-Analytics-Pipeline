# The ML job orchestrator

# imports
import requests
import json
from prefect import flow, task

# helper function - generic invoker
def invoke_gcf(url:str, payload:dict):
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

@task(retries=2)
def schema_setup():
    """Setup the stage schema"""
    url = "https://us-central1-ba882-inclass-project.cloudfunctions.net/mlops-schema-setup"
    resp = invoke_gcf(url, payload={})
    return resp

@task(retries=2)
def train_movies():
    """Train the model against movies data from the cloud warehouse"""
    url = "https://us-central1-ba882-inclass-project.cloudfunctions.net/mlops-movies-trainer"
    resp = invoke_gcf(url, payload={})
    return resp

@task(retries=2)
def train_shows():
    """Train the model against shows data from the cloud warehouse"""
    url = "https://us-central1-ba882-inclass-project.cloudfunctions.net/mlops-shows-trainer"
    resp = invoke_gcf(url, payload={})
    return resp

# Prefect Flow
@flow(name="mlops-recommendation-model", log_prints=True)
def training_flow():
    """The ETL flow which orchestrates Cloud Functions for the ML task"""
    
    result = schema_setup()
    print("The schema setup completed")

    stats_movies = train_movies()
    print("The model training for movies completed successfully")
    print(f"{stats_movies}")

    stats_shows = train_shows()
    print("The model training for shows completed successfully")
    print(f"{stats_shows}")

# the job
if __name__ == "__main__":
    training_flow()
