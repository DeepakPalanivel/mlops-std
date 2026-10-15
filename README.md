# Student Result Predictor — CodePipeline EC2 Deploy Action (No CodeDeploy)

Adapted to the supplied reference: GitHub → CodePipeline V2 → Amazon EC2 Deploy action via Systems Manager (SSM). No CodeDeploy agent, appspec.yml, Docker, or GitHub Actions is used in this version.

## Files
- `train.py`: trains the demo model and saves model version with it.
- `app.py`: Flask application.
- `templates/index.html`: prediction form.
- `requirements.txt`: Python dependencies.
- `deploy-scripts/deploy.sh`: installs dependencies, trains the model, and restarts the service.

## AWS setup summary
1. Upload all files to GitHub repository `ml-app`, branch `main`.
2. Launch Ubuntu EC2; tag `Name = EC2DeployDemo`.
3. Security group: SSH 22 restricted to your IP; HTTP 80 open to `0.0.0.0/0`.
4. Attach EC2 IAM role with `AmazonSSMManagedInstanceCore` and `AmazonS3ReadOnlyAccess`.
5. Wait for the instance to show Online in Systems Manager Fleet Manager.
6. Create CodePipeline V2 with GitHub (via GitHub App) as Source; skip Build and Test.
7. Select Amazon EC2 as Deploy provider and configure:
   - Instance type: EC2
   - Instance tag key: `Name`
   - Instance tag value: `EC2DeployDemo`
   - Target directory: `/home/ubuntu/ml-app`
   - Post-script: `deploy-scripts/deploy.sh`
8. If the first deployment fails with access denied, inspect the pipeline service role permissions as described in the reference.

## Verify automatic deployment
Open `http://YOUR_EC2_PUBLIC_IP`. To test version 2.0, change `MODEL_VERSION = "1.0"` to `MODEL_VERSION = "2.0"` in `train.py`, commit to `main`, wait for CodePipeline to finish, then refresh the page.

Troubleshooting:
```bash
sudo systemctl status ml-app
sudo journalctl -u ml-app -n 50
```

The sample dataset is synthetic and not suitable for real student grading. AWS resources may incur charges; delete the pipeline, artifact bucket, and EC2 after evaluation.
