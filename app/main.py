import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from predict_flair import make_single_prediction, make_multiple_prediction
import sys

sys.path.append("")
app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']

    processed_text = make_single_prediction(text)
    if processed_text == 0:
    	to_return = "Invalid URL"
    else:
    	to_return = "The submission had the flair: " + processed_text[0]
    return to_return

@app.route('/automated_testing', methods=['POST', 'GET'])
def getfile():
	if request.method == 'POST':

		# for secure filenames. Read the documentation.
		#print(request.files)
		file = request.files['file']
		filename = secure_filename(file.filename) 

		# os.path.join is used so that paths work in every operating system
		file_content = file.readlines()
		file_content = [i.decode('utf-8') for i in file_content]
		#print(file_content)
		#file.save(os.path.join("",filename))

		# You should use os.path.join here too.
		#with open("filename") as f:
		to_return = make_multiple_prediction(file_content)
		return to_return

	else:
		print(request.args)
		result = request.args.get['file']
	return file_content