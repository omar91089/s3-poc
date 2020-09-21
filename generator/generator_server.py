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
    log_str = '[GENERATOR SERVER] File: {0}, was processed with /submit_status API with status: {1}'.format(file_name, status)
    print(log_str)
    return log_str
