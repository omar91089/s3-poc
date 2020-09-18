from flask import Flask
app = Flask(__name__)


@app.route('/process-file')
def hello_world():
    return 'Hello, World!'
