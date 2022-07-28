# Jupyter In Docker 
Python Flask App

# Init:
Install nvidia-docker-container and pull
```bash
docker pull tensorflow/tensorflow:latest-gpu-jupyter
```
```bash
python3 -m venv ./venv
```
```bash
source ./venv/bin/activate
```
```bash
python -m pip install --upgrade pip
```
```bash
python -m pip install -r requirements.txt
```
# Install nginx and run:
```bash
sudo cp nginx/jtainer.conf /etc/nginx/conf.d
```
# Restart nginx
```bash
sudo systemctl restart nginx
```

# Install ngrok and run tunnel
```bash
./ngrok http 8080
```
# Run app.py
Change image_docker in app.py to your docker image name, e.g: tensorflow:jupyter-gpu-latest

```bash
python app.py
```
# Register and get token at
http://localhost:8080/app/register

# Your notebook will run at 
http://localhost:8080