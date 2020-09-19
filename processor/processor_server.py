from flask import Flask
from .processor import process_file

app = Flask(__name__)


@app.route('/')
def server_info():
    return 'Consumer server is running!'


@app.route('/process-file', methods=['POST'])
def process_file():
    req_data = request.get_json()
    file_name = req_data.get('file_name')
    bucket_name = req_data.get('bucket_name')
    key_name = req_data.get('key_name')

    process_file(file_name, bucket_name, key_name)
    return 'Successfully submitted file for processing!'
