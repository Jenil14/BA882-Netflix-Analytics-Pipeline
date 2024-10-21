import pandas as pd
from google.cloud import storage
import datetime
import uuid
from io import BytesIO
import functions_framework
import requests

# storage client
storage_client = storage.Client()

# storage bucket
bucket_name = "ba882-team05"

# file URLs
file_urls = {
    "netflix_countries": "https://www.netflix.com/tudum/top10/data/all-weeks-countries.tsv",
    "netflix_global": "https://www.netflix.com/tudum/top10/data/all-weeks-global.tsv",
    "netflix_most_popular": "https://www.netflix.com/tudum/top10/data/most-popular.tsv"
}

@functions_framework.http
def main(request):
    
    results = {}

    for dataset, url in file_urls.items():
        
        # Generate job ID
        JOB_ID = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "-" + str(uuid.uuid4())
        
        response = requests.get(url)

        if response.status_code == 200:
            # Define blob name based on the dataset
            blob_name = f"jobs/{dataset}/{JOB_ID}/{dataset}.json"

            # Use BytesIO directly with response.content
            df = pd.read_csv(BytesIO(response.content), sep='\t')

            # Convert DataFrame to JSON
            json_data = df.to_json(orient='records', lines=True)

            # Upload to GCS
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.upload_from_string(json_data, content_type='application/json')

            # Store the result
            results[dataset] = {
                'status': 'success',
                'blob_name': blob_name
            }
        else:
            results[dataset] = {
                'status': 'error',
                'message': f'Failed to fetch data for {dataset}',
                'status_code': response.status_code
            }

    # Check if all datasets were processed successfully
    if all(result['status'] == 'success' for result in results.values()):
        return {
            'message': 'All datasets processed successfully',
            'job_id': JOB_ID,
            'results': results
        }, 200
    else:
        return {
            'message': 'Some datasets failed to process',
            'job_id': JOB_ID,
            'results': results
        }, 500