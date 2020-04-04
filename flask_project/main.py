import os
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from pathlib import Path

from flask_project.src.convert_to_tsv import Converter
from flask_project.src.map_labels_to_tsv import LabelMapper

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

converter = Converter()
mapper = LabelMapper()


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():

	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			root_dir = os.path.join(app.config['UPLOAD_FOLDER'], Path(filename).stem)
			os.makedirs(root_dir, exist_ok=True)
			file.save(os.path.join(root_dir, filename))
			flash('File successfully uploaded')
			tsv_path = converter.convert_pdf(filename)
			mapper.extract_and_write_result_for_document(tsv_path)

			return redirect('/')
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return redirect(request.url)

if __name__ == "__main__":
    app.run()
