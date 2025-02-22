######
## simple script for now to deploy functions
## deploys all, which may not be necessary for unchanged resources
######

# setup the project
gcloud config set project ba882-inclass-project

# schema setup
echo "======================================================"
echo "deploying the schema setup"
echo "======================================================"

gcloud functions deploy mlops-schema-setup \
    --gen2 \
    --runtime python311 \
    --trigger-http \
    --entry-point task \
    --source /home/sekka/BA882-Team05-Project/ml/pipeline/functions/schema-setup \
    --stage-bucket ba882-team05-functions \
    --service-account id-82-group-project@ba882-inclass-project.iam.gserviceaccount.com \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 512MB  \
    --timeout 540s 

# the training module
echo "======================================================"
echo "deploying the movies trainer"
echo "======================================================"

gcloud functions deploy mlops-movies-trainer \
    --gen2 \
    --runtime python311 \
    --trigger-http \
    --entry-point task \
    --source /home/sekka/BA882-Team05-Project/ml/pipeline/functions/movies-trainer \
    --stage-bucket ba882-team05-functions \
    --service-account id-82-group-project@ba882-inclass-project.iam.gserviceaccount.com \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 1GB  \
    --timeout 540s

# the training module
echo "======================================================"
echo "deploying the shows trainer"
echo "======================================================"

gcloud functions deploy mlops-shows-trainer \
    --gen2 \
    --runtime python311 \
    --trigger-http \
    --entry-point task \
    --source /home/sekka/BA882-Team05-Project/ml/pipeline/functions/shows-trainer \
    --stage-bucket ba882-team05-functions \
    --service-account id-82-group-project@ba882-inclass-project.iam.gserviceaccount.com \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 1GB  \
    --timeout 540s

# the predictions function
echo "======================================================"
echo "deploying dynamic prediction endpoint"
echo "======================================================"

gcloud functions deploy mlops-prediction \
    --gen2 \
    --runtime python311 \
    --trigger-http \
    --entry-point task \
    --source /home/sekka/BA882-Team05-Project/ml/pipeline/functions/prediction \
    --stage-bucket ba882-team05-functions \
    --service-account id-82-group-project@ba882-inclass-project.iam.gserviceaccount.com \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 1GB