import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
#from predict_flair import make_single_prediction, make_multiple_prediction
import sys

import json
import praw
import joblib
import re
from nltk.corpus import stopwords
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

from bs4 import BeautifulSoup



sys.path.append("")
app = Flask(__name__)

def clean_text(text):
    soup = BeautifulSoup(text, "lxml")
    text = soup.text
    text = text.lower()
    text = REPLACE_BY_SPACE_RE.sub(' ', text)
    text = BAD_SYMBOLS_RE.sub('', text)
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    return text

def to_string(s):
    return str(s)

def get_date(created):
    return dt.datetime.fromtimestamp(created)

def get_comments(s):
	co=0
	comment = ""
	for top_level_comment in s.comments:
		comment = comment + ' ' + top_level_comment.body
		co+=1
		if co>10:
			break
		return comment

def make_single_prediction(url):
	try:
		reddit = praw.Reddit(user_agent='reddit_scrapper',client_id='JTHhWnxWZscuMQ',client_secret="3IqQuupFVVlXJDmqBBPSSzkXYn8",username='ChetanMadan', password='Alwaysbehappy.12')

		#url = 'https://www.reddit.com/r/india/comments/g1zi21/coronavirus_covid19_megathread_news_and_updates_4/'
		sub = praw.models.Submission(reddit, url = url)

		title = clean_text(str(sub.title))
		comments = clean_text(get_comments(sub))
		url = str(sub.url)
		body = clean_text(str(sub.selftext))
		features = title + comments + url + body


		model = joblib.load('gb_model.sav')
		flair = model.predict([features])
	except praw.exceptions.ClientException:
		flair = 0

	#print(features, str(sub.link_flair_text))
	return flair


def make_multiple_prediction(urls):

	reddit = praw.Reddit(user_agent='reddit_scrapper',client_id='JTHhWnxWZscuMQ',client_secret="3IqQuupFVVlXJDmqBBPSSzkXYn8",username='ChetanMadan', password='Alwaysbehappy.12')
	flairs = {}
	for url in urls:
		try:
			sub = praw.models.Submission(reddit, url = url)
			title = clean_text(str(sub.title))
			comments = clean_text(get_comments(sub))
			url = str(sub.url)
			body = clean_text(str(sub.selftext))
			features = title + comments + url + body


			model = joblib.load('gb_model.sav')
			flair = model.predict([features])
			flairs[url] = flair[0]
		except praw.exceptions.ClientException:
			flairs[url] = "Invalid URL"
	#print(features, str(sub.link_flair_text))
	return json.dumps(flairs)
	

@app.route('/')
def my_form():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']

    processed_text = make_single_prediction(text)
    if processed_text == 0:
    	to_return = "Invalid URL"
    	return render_template('result.html', data = [to_return, ""])
    else:
    	to_return = "The submission with URL: {} had the flair: ".format(text)
    	return render_template('result.html', data = [to_return, processed_text[0]])


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