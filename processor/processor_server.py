from flask import Flask, request
from .processor import process_and_transfer_file, TransferStrategy

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

    process_and_transfer_file(TransferStrategy(), file_name, bucket_name, key_name)
    log_str = '[PROCESSOR SERVER] Successfully submitted file for processing using /process_file API!'
    print(log_str)
    return log_str
