import praw
import joblib
import re
from nltk.corpus import stopwords
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

from bs4 import BeautifulSoup
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
	return flairs
	