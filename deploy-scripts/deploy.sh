#!/bin/bash
set -e
APP_DIR=/home/ubuntu/ml-app
VENV=/opt/ml-venv

apt-get update -y
apt-get install -y python3-venv python3-pip

if [ ! -d "$VENV" ]; then
    python3 -m venv "$VENV"
fi

cd "$APP_DIR"
"$VENV/bin/pip" install --no-cache-dir -r requirements.txt
"$VENV/bin/python" train.py

# Stop Nginx if an earlier lab left it using port 80.
systemctl disable --now nginx 2>/dev/null || true

cat > /etc/systemd/system/ml-app.service <<SERVICE
[Unit]
Description=Student Result Predictor
After=network.target

[Service]
WorkingDirectory=$APP_DIR
ExecStart=$VENV/bin/gunicorn --workers 2 --bind 0.0.0.0:80 app:app
Restart=always
User=root

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable ml-app
systemctl restart ml-app
sleep 2
systemctl --no-pager --full status ml-app
echo "Student Result Predictor deployed successfully."
