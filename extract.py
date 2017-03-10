# encoding=utf-8

from bs4 import BeautifulSoup
from pandas import DataFrame

def load_tags():
	soup = BeautifulSoup(open('tags.html').read(), "html.parser")
	tags = soup.find_all("a")
	for tag in tags:
		print(tag.get_text()+":"+tag['title'].encode('utf-8').replace('个话题', ''))

if __name__ == "__main__":
	load_tags()
