docker build -t gcr.io/teak-listener-435221-g2/flask-api .

docker push gcr.io/teak-listener-435221-g2/flask-api

gcloud run deploy flask-api \
  --image gcr.io/teak-listener-435221-g2/flask-api \
  --platform managed \
  --region us-east1 \
  --allow-unauthenticated