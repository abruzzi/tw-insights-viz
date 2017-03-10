# encoding=utf-8

import feedparser
import jieba
import urllib2
from bs4 import BeautifulSoup
from collections import Counter
from pandas import DataFrame

# def extract_post_content(entry):
# 	page = urllib2.urlopen(entry.link).read()
# 	soup = BeautifulSoup(page, "html.parser")
	
# 	return soup.find('div', attrs={'class': 'entry-content'}).text
	
	# print(soup.find('article', class_='post').text)
	# return soup.find('article', class_='post').text

def extract_post_content(file):
	soup = BeautifulSoup(open(file).read(), "html.parser")
	return soup.find('div', attrs={'class': 'entry-content'}).text

# def fetch_feeds(feed_url='http://insights.thoughtworkers.org/feed/'):
# 	feed = feedparser.parse(feed_url)
# 	return map(extract_post_content, feed.entries)
	
def fetch_feeds():
	return []

def extract_segments(data):
	seg_list = jieba.cut(data, cut_all=False)
	return [seg.strip() for seg in seg_list if len(seg) > 1]

def tokenize():	
	stoplist = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
	stoplist.extend(['...', 'com', 'using', u'使用', 'blog', u'博客', u'博客园', u'做法', u'论坛', 'part', u'部分', u'天下'])
	
	filtered = map(extract_segments, fetch_feeds())

	tokens = Counter([word for words_in_article in filtered 
		for word in words_in_article 
		if word not in stoplist])

	return DataFrame(tokens.most_common(20), columns=['keywords', 'frequencies'])
	# for words_in_article in filtered:
	# 	return Counter([word for word in filtered if word not in stoplist])
	# 	for word in words_in_article:
	# 		print(word)
	# filtered = extract_segments(fetch_feeds())
	# print_out(filtered)

# print(tokenize())

def extract_all_text():
	with open('filepaths') as f:
	    content = f.readlines()

	file_list = [x.strip() for x in content]
	return map(extract_post_content, file_list)

# for file in file_list:
# 	print extract_post_content(file)

print extract_all_text()
# print(file_list)