from flask import Flask, render_template, request, flash, redirect, url_for
from azure.storage.blob import BlockBlobService, PublicAccess
from werkzeug.utils import secure_filename
import os
import requests

app = Flask(__name__)

block_blob_service = BlockBlobService(account_name='storagedicoding', account_key='y+onmJ455oyG8Idt/I3A0nfWCo6eCzMcHR6cGoRKKNYbj7hIlAdcvv75HQT6AquIBhH/Y+eNUUlOGkuv2JXhGw==')

# Create a container called 'quickstartblobs'.
container_name = 'quickstartblobs'

# Create a container called 'quickstartblobs'.
block_blob_service.create_container(container_name)

# Set the permission so the blobs are public.
block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

#computer vision 
headers = {
    'Ocp-Apim-Subscription-Key': 'fa09f72343ae4bc9bcd5f5a2b6ec6df5',
    'Content-Type': 'application/json',
}

params = (
    ('visualFeatures', 'Categories,Description'),
    ('details', 'Landmarks'),
    ('language', 'en'),
)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            block_blob_service.create_blob_from_stream(container_name, "blob_images", file )
            return redirect(url_for('analyze_file'))
    return render_template('index.html')

@app.route('/analyze')
def analyze_file():
    data = '{"url":"https://storagedicoding.blob.core.windows.net/quickstartblobs/blob_images"}'
    uri = data.split('"')[3]
    response = requests.post('https://southeastasia.api.cognitive.microsoft.com//vision/v2.0/analyze', headers=headers, params=params, data=data)
    return render_template('analyze.html', uri = uri, response = response.text)
