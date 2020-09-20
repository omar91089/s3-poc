from flask import Flask, request
from .processor import process_file

app = Flask(__name__)


@app.route('/')
def server_info():
    return 'Processor server is running!'


@app.route('/process_file', methods=['POST'])
def process_file_server():
    req_data = request.get_json()
    file_name = req_data.get('file_name')
    bucket_name = req_data.get('bucket_name')
    key_name = req_data.get('key_name')

    process_file(file_name, bucket_name, key_name)
    return 'Successfully submitted file for processing!'
