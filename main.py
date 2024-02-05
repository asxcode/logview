import os
from flask import Flask, request, jsonify, render_template, send_file
from datetime import datetime
from zipfile import ZipFile
from datetime import datetime

# Get today's date
today_date = datetime.now()

# Format it as yyyymmdd
today_date = today_date.strftime('%Y%m%d')

app = Flask(__name__)


def convert_date_format(input_date):
    # Convert string to datetime object
    date_object = datetime.strptime(input_date, '%Y%m%d')

    # Format the datetime object to the desired format
    formatted_date = date_object.strftime('%d/%m/%Y')

    return formatted_date

@app.route('/')
def index():
    directory_path = 'data/logs'

    # Get a list of files in the directory
    date_dirs = os.listdir(directory_path)

    processed_date_dirs = []

    for dir_name in date_dirs:
        p_ele = {}
        p_ele['dirname'] = convert_date_format(dir_name)
        p_ele['date'] = dir_name
        processed_date_dirs.append(p_ele)

    print(processed_date_dirs)

    return render_template('index.html', date_dirs=processed_date_dirs)


@app.route('/logs/<date>/error')
def error_logs(date):
    try:
        filepath = 'data/logs/' + date + '/error.txt'
        with open(filepath, 'r') as file:
            content = file.read()

        # Create a dictionary to represent the JSON response
        response_data = {
            'status': 'success',
            'content': content
        }

        # Convert the dictionary to JSON and return as a response
        return jsonify(response_data)

    except Exception as e:
        # Handle any exceptions (e.g., file not found)
        response_data = {
            'status': 'error',
            'message': str(e)
        }
        return jsonify(response_data), 500  # 500 is the HTTP status code for Internal Server Error


@app.route('/logs/<date>/warning')
def warning_logs(date):

    return date


@app.route('/logs/<date>/sos')
def sos_logs(date):

    return date


@app.route('/logs/<date>/debug')
def debug_logs(date):

    return date


@app.route('/logs/<date>/activity')
def user_activites(date):

    return date


@app.route('/download/<date>')
def download_directory(date):
    try:
        directory_to_zip = 'data/logs/' + date

        # Create a temporary zip file
        zip_filename = date + '-logview.zip'
        zip_path = os.path.join('tmp', zip_filename)

        with ZipFile(zip_path, 'w') as zipf:
            for root, dirs, files in os.walk(directory_to_zip):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, directory_to_zip)
                    zipf.write(file_path, arcname=arcname)
            
        # # Send the zip file as a response
        return send_file(zip_path, as_attachment=True, download_name=date + '-logview.zip')

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500  # 500 is the HTTP status code for Internal Server Error


@app.route('/receive/<logtype>', methods=['POST'])
def receive_logs(logtype):
    try:
        # Ensure the 'logs' key is present in the request
        if 'logs' not in request.files:
            return jsonify({'status': 'error', 'message': 'No log file provided'}), 400  # 400 is the HTTP status code for Bad Request

        if logtype not in ['error', 'info', 'warning', 'sos', 'debug', 'activity', 'info']:
            logtype = 'info'
        
        log_file = request.files['logs']

        # Specify the directory path
        directory_path = f'data/logs/{today_date}'

        # Check if the directory exists
        if not os.path.exists(directory_path):
            # Create the directory if it doesn't exist
            os.makedirs(directory_path)
            print(f'Directory "{directory_path}" created.')


        # Specify the directory where you want to save the log file
        save_path = os.path.join("data/logs/" + today_date, logtype + '.txt')
        log_file.save(save_path)

        # Process and store logs as needed
        # You might want to handle log storage, parsing, or any other custom logic here

        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500  # 500 is the HTTP status code for Internal Server Error

if __name__ == '__main__':
    print(today_date)
    app.run(debug=True)
