from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def server_info():
    return 'Generator Server is running!'


@app.route('/submit_status', methods=['POST'])
def submit_status():
    req_data = request.get_json()
    status = req_data.get('status')
    file_name = req_data.get('file_name')
    return 'File: {0}, was processed with status: {1}'.format(file_name, status)
