from crypt import methods
from lib2to3.pgen2 import token
import re
from flask import Flask, request, json, redirect, url_for
from flask import render_template
import uuid
import datetime
import time 
import threading 
import subprocess
import os

app = Flask(__name__)
app.debug = True

secret_password = '123456'
admin_password = 'freegpu'
image_docker = 'jupyter:ubuntu'

in_use = False
timeout = None

def countdown(container_id):
    global timeout, in_use
    
    while True:
        
        if timeout - time.time() >= 0:
            continue
        else:
            in_use = False
            timeout = None
            cmd = ["docker","stop", container_id]
            subprocess.run(cmd)
            print('timeout')
            break
        
@app.route('/')
def home():
    return "Hello world!!!"
      
@app.route("/app/register", methods=["GET", "POST"])
def register():
    global in_use, timeout
    
    if request.method == 'GET':
        if not in_use:
            return render_template('index.html')
        else:
            t  = (timeout - time.time())/3600
            return json.dumps({
            "status": f"Server is running, please wait for {t} h" })

    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        limited = request.form['limited']
        
        if username and password:
            return validateUser(email, username, password, limited)
        
        return json.dumps({'validation' : False})

@app.route("/app/generate_new_password/<admin>")
def gnp(admin):
    global secret_password, admin_password
    secret_password = uuid.uuid4().hex
    if admin== admin_password:
        return json.dumps({
            "password":  secret_password
        })
        
@app.route('/app/users')
def user():
    with open('user.txt', 'r') as files:
        x = files.read()
    return json.dumps(x)

def validateUser(email, username, passwords, limited):
    global secret_password, in_use, timeout
    
    if passwords == secret_password:
        in_use = True
        timeout = time.time() + int(limited)*3600
        
        with open('user.txt', 'a') as the_file:
            the_file.write(f'{email} {username} {datetime.datetime.utcnow()} time limited {limited} \n')
        

        results = subprocess.run(f"docker run -d --rm -p 9999:9090 {image_docker} jupyter notebook --ip 0.0.0.0 --no-browser --port=9090 --allow-root", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        container_id = str(results.stdout.decode('utf-8')[:12])

        thread =  threading.Thread(target=countdown, args=(str(container_id),))
        thread.daemon = True
        thread.start()
        time.sleep(5)
        stream = os.popen(f'docker exec {container_id} jupyter notebook list')
        #print(stream.read())
        token_id = stream.read()

        return json.dumps({'validation' : token_id})
    
    else:
        return json.dumps({'validation' : False})
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')