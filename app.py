from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return {"about":"Hello Flask App!!!"}

@app.route('/healthy', methods=['GET', 'POST'])
def healthy():
    return "<H2>Flask App is Healthy!!!</H2>"

@app.route('/login', methods=['POST'])
def login():
    content = request.get_json(force=True)
    return {"Message" : content}, 201