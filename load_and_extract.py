# encoding=utf-8

import jieba
import jieba.analyse
from bs4 import BeautifulSoup
from collections import Counter
from pandas import DataFrame

def extract_post_content(file):
    soup = BeautifulSoup(open(file).read(), "html.parser")
    return soup.find('div', attrs={'class': 'entry-content'}).text
    
def fetch_feeds():
    return []

def extract_segments(data):
    seg_list = jieba.cut(data, cut_all=False)
    return [seg.strip() for seg in seg_list if len(seg) > 1]

def tokenize(): 
    stoplist = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
    
    filtered = map(extract_segments, extract_all_text())

    tokens = Counter([word for words_in_article in filtered 
        for word in words_in_article 
        if word not in stoplist])

    return DataFrame(tokens.most_common(20), columns=['keywords', 'frequencies'])

# print(tokenize())

def extract_all_text():
    with open('filepaths') as f:
        content = f.readlines()

    file_list = [x.strip() for x in content]
    return map(extract_post_content, file_list)

# print tokenize()


def taging(content):
    return ",".join(jieba.analyse.extract_tags(content, topK=32))

# open('tags', "w").write("\n".join(map(taging, extract_all_text())).encode('utf-8'))
# for content in extract_all_text():
#   tags = jieba.analyse.extract_tags(content, topK=32)
#   print(",".join(tags))

# content = "\n".join(extract_all_text())

# open("all_text", "w").write(content.encode('utf-8'))

# tags = jieba.analyse.extract_tags(content, topK=100)
# print(",".join(tags))

from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


import sys
import string

reload(sys)
sys.setdefaultencoding('utf8')

def tfidf_calc():        
    # segments = extract_segments("\n".join(extract_all_text()))

    corpus = [" ".join(item) for item in map(extract_segments, extract_all_text())]
    # with open('segments', "w") as f:
    #     f.write("\n".join(segments).encode('utf-8'))
    # print corpus

    # vectorizer = CountVectorizer()
    # vectorizer.fit_transform(corpus)
    
    with open('stopwords-utf8.txt') as f:
        content = f.readlines()

    content.extend(['来说', '事情', '提供', '带来', '发现'])
    stopwords = [x.strip().decode('utf-8') for x in content]

    vectorizer = TfidfVectorizer(min_df=1, smooth_idf=False, sublinear_tf=True, stop_words=stopwords)
    vectorizer.fit_transform(corpus)

    data = dict(zip(vectorizer.get_feature_names(), vectorizer.idf_))
    result = DataFrame(data.items(), columns=['word', 'tfidf']).sort_values(by='tfidf', ascending=True).head(50)

    result.to_csv('top-50-words-in-tw-insight.csv')
    # print(result)

    # # print vectorizer.vocabulary_

    # for key, value in data.iteritems():
    #     print key.encode('utf-8'), value

    # print vectorizer.vocabulary

    # transformer = TfidfTransformer(smooth_idf=False)
    # tfidf = transformer.fit_transform(vectorizer.fit_transform(segments))

    # word = vectorizer.get_feature_names()
    # weight = tfidf.toarray()

    # result = []
    # for i in range(len(weight)):
    #     for j in range(len(word)):
    #         result.append((word[j] + " " + str(weight[i][j])).encode('utf-8'))

    # with open('feature_names_mem', "w") as f:
    #     f.write("\n".join(result))

    # with open('feature_names', "w") as f:
    #     for i in range(len(weight)):
    #         for j in range(len(word)):
    #             f.write((word[j] + " " + str(weight[i][j]) + "\n").encode('utf-8'))

tfidf_calc()