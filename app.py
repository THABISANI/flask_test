from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return {"about":"Hello Flask App!!!"}

@app.route('/healthy', methods=['GET', 'POST'])
def healthy():
    return "<H1>Flask App is Healthy!!!</H1>"