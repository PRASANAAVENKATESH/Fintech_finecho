import os
import io
import zipfile
from Flask import Flask, redirect, url_for, render_template, request, session
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
import signal
import gdown
import subprocess

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

UPLOAD_FOLDER = 'uploads'

def cleanup_on_exit(signum, frame):
    print("Received termination signal. Cleaning up...")

    # Clean up uploaded files
    files_in_uploads = os.listdir(UPLOAD_FOLDER)
    for filename in files_in_uploads:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            os.remove(file_path)

    # Clean up llmdata.txt
    llmdata_file_path = "llmdata.txt"
    if os.path.exists(llmdata_file_path):
        os.remove(llmdata_file_path)

    # Clean up contents of visualization folder
    visualization_folder = "visualization"
    if os.path.exists(visualization_folder) and os.path.isdir(visualization_folder):
        files_in_visualization = os.listdir(visualization_folder)
        for filename in files_in_visualization:
            file_path = os.path.join(visualization_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    print("Cleanup successful")
    exit(0)

        

def start_llmdata_if_data_present():
    csv_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.csv')]
    if csv_files:
        print("CSV files found in uploads folder. Starting llmdata.py...")
        subprocess.Popen(["python", "llmdata.py"])
    else:
        print("No CSV files found in uploads folder. llmdata.py not started.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']


    if username == 'admin' and password == '1234':
        return redirect(url_for('data'))
    else:
        return redirect(url_for('index'))

@app.route('/data')
def data():
    return render_template('indata.html')

@app.route('/local', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'localFile' in request.files:
            file = request.files['localFile']
            if file.filename != '':
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)
                if os.path.exists(file_path):
                    start_llmdata_if_data_present()  # Check for CSV files after file upload
                    return redirect(url_for('success'))
    return render_template('local.html')

# cloud 
class DataIngestionConfig:
    def __init__(self, source_URL: str, local_data_file: str, unzip_dir: str):
        self.source_URL = source_URL
        self.local_data_file = local_data_file
        self.unzip_dir = unzip_dir

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file_from_drive(self) -> None:
        try: 
            dataset_url = self.config.source_URL
            zip_download_dir = self.config.local_data_file

            print(f"Downloading data from {dataset_url} into file {zip_download_dir}")

            file_id = dataset_url.split("/")[-2]
            prefix = 'https://drive.google.com/uc?/export=download&id='
            gdown.download(prefix + file_id, zip_download_dir, quiet=False)

            print(f"Downloaded data from {dataset_url} into file {zip_download_dir}")

        except Exception as e:
            raise e
        
    
    def extract_zip_file(self) -> None:
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)

@app.route('/cloud', methods=['GET', 'POST'])
def local():
    if request.method == 'POST':
        drive_link = request.form.get('drive_link')
        config = DataIngestionConfig(
            source_URL=drive_link,
            local_data_file="uploads/downloaded_file.zip",
            unzip_dir="uploads"
        )
        data_ingestion = DataIngestion(config)
        data_ingestion.download_file_from_drive()
        data_ingestion.extract_zip_file()

        downloaded_file_path = os.path.join("uploads", "downloaded_file.zip")
        if os.path.exists(downloaded_file_path):
            print("File exists, redirecting to link.html")
            session['file_downloaded'] = True 
            start_llmdata_if_data_present()  # Start llmdata.py if data is present
            return redirect(url_for('link'))
        else:
            print("File does not exist, something went wrong")
            session['file_downloaded'] = False 
            return redirect(url_for('cloud'))  

    return render_template('cloud.html')

@app.route('/link')
def link():
    if session.get('file_downloaded'):
        return render_template('link.html')
    else:
        return redirect(url_for('cloud'))  

@app.route('/start-app', methods=['POST'])
def start_app():
    streamlit_process = subprocess.Popen(["streamlit", "run", "app.py"])
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('link.html')

@app.route('/move_to_gpt', methods=['GET'])
def move_to_gpt():
    return render_template('gpt.html')

if __name__ == '__main__':
    signal.signal(signal.SIGINT, cleanup_on_exit)  
    start_llmdata_if_data_present()  # Start llmdata.py if data is already present when the server starts
    app.run(debug=True)
