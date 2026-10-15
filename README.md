# Student Result Predictor — Docker on EC2 with CodePipeline EC2 Deploy action

This version runs the Flask/ML app inside a Docker container on EC2 and uses the supplied reference workflow: GitHub → AWS CodePipeline V2 → Amazon EC2 Deploy action via Systems Manager (SSM). No CodeDeploy agent or appspec.yml is used.

## Files
- `train.py`: trains the model and saves model version.
- `app.py`: Flask web application.
- `templates/index.html`: prediction form.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: builds the app image and trains the model during image build.
- `deploy-scripts/deploy.sh`: builds the image and replaces the running container.

## GitHub
Upload all files/folders to repository `ml-app`, branch `main`.

## EC2 prerequisites
Launch Ubuntu EC2, tag it `Name = EC2DeployDemo`. Security group inbound rules: SSH (22) from your IP; HTTP (80) from `0.0.0.0/0`. Attach an EC2 IAM role with `AmazonSSMManagedInstanceCore` and `AmazonS3ReadOnlyAccess`. Wait until Systems Manager Fleet Manager shows the instance Online.

Docker must be installed on EC2 before the pipeline deploys. Connect to EC2 and run:
```bash
sudo apt update
sudo apt install -y docker.io git
sudo systemctl enable --now docker
sudo mkdir -p /home/ubuntu/ml-app
sudo chown -R ubuntu:ubuntu /home/ubuntu/ml-app
```
The EC2 Deploy action will place the repository revision in `/home/ubuntu/ml-app`.

## CodePipeline
Create a V2 pipeline with GitHub (via GitHub App) Source, skip Build and Test, then choose Amazon EC2 as Deploy provider:
- Instance type: EC2
- Instance tag key: `Name`
- Instance tag value: `EC2DeployDemo`
- Target directory: `/home/ubuntu/ml-app`
- Post-script: `deploy-scripts/deploy.sh`

If the EC2 Deploy action cannot find Docker, confirm Docker is installed and that the script runs with sufficient privileges. The reference action's post-script runs on the instance; if the action does not execute as root, use `sudo docker` commands in the script or configure permissions appropriately.

## Automatic deployment test
Open `http://YOUR_EC2_PUBLIC_IP`. Change `MODEL_VERSION = "1.0"` to `"2.0"` in `train.py`, commit to `main`, wait for CodePipeline to succeed, and refresh the page. Each deployment rebuilds the image, retrains the model, and replaces the container.

This uses synthetic demonstration data, not validated for real student grading. AWS resources may incur charges; clean up after evaluation.
