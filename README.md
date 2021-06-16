The purpose of this package is to process requests for our test application from our mobile clients.

## Install Python

```bash
sudo yum install python3 -y
```

## Install Flask

```bash
sudo pip3 install Flask
```

## Now, set the envs and run your flask Application

```bash
export FLASK_APP=flaskblog.py
export FLASK_DEBUG=1
flask run 
```