#!/bin/bash
set -e

APP_DIR=/home/ubuntu/ml-app
cd "$APP_DIR"

# Build the Docker image from the revision downloaded by CodePipeline.
docker build -t student-app:latest .

# The version is saved in the model by train.py during image build.
# Replace the previous container and publish Flask on public HTTP port 80.
docker rm -f student-app 2>/dev/null || true
docker run -d --name student-app --restart unless-stopped -p 80:5000 student-app:latest

sleep 3
if ! docker ps --filter "name=student-app" --filter "status=running" | grep -q student-app; then
  docker logs student-app || true
  exit 1
fi
echo "Student Result Predictor Docker container deployed."
