## ThoughtWorks的洞见讲什么？



### 数据获取

本来打算用`feedparser`从`RSS`上读feed，然后解析出文章的`link`，将所有文章爬一遍，最后保存到本地。不过中间发现Wordpress默认地只输出最新的`feed`，这会降低最后关键字列表的精度。毕竟语料库越大，效果越好。

既然是一个静态站点，最简单，最暴力的方式是直接把站点克隆到本地，使用`wget`很容易做到：

```sh
wget --mirror -p --html-extension --convert-links -e robots=off -P . http://insights.thoughtworkers.org/
```

默认地，`wget`会以站点的完整域名为目录名，然后保存整个站点到本地。我大概看了一下，其实不需要所有的目录，只需要一个层次即可，所以用`find`来过滤一下，然后将文件名写到一个本地文件`filepaths`中。

```sh
find insights.thoughtworkers.org/ -name index.html -depth 2 > filepaths
```

这个文件的内容是这样的：

```
insights.thoughtworkers.org/10-common-questions-of-ba/index.html
insights.thoughtworkers.org/10-tips-for-good-offshore-ba/index.html
insights.thoughtworkers.org/10-ways-improve-your-pairing-experience/index.html
insights.thoughtworkers.org/100-years-computer-science/index.html
insights.thoughtworkers.org/1000-cars-improve-beijing-transportation/index.html
insights.thoughtworkers.org/3d-printing/index.html
insights.thoughtworkers.org/4-advices-for-aid/index.html
insights.thoughtworkers.org/5-appointments-with-agile-team/index.html
insights.thoughtworkers.org/5-ways-exercise-visual-design/index.html
insights.thoughtworkers.org/7-step-agenda-effective-retrospective/index.html
insights.thoughtworkers.org/a-decade/index.html
insights.thoughtworkers.org/about-team-culture/index.html
insights.thoughtworkers.org/about-tw-insights/index.html
insights.thoughtworkers.org/agile-coach/index.html
insights.thoughtworkers.org/agile-communication/index.html
insights.thoughtworkers.org/agile-craftman/index.html
...
```

### 数据处理

这样我就可以很容易在python脚本中读取各个文件并做处理了。有了文件之后，需要做这样一些事情：

1.  抽取HTML中的文本信息
1.  将文本分词成列表
1.  计算列表中所有词的TFIDF值
1.  将结果持久化到本地

这里需要用到这样一些pyhton库：

1.  BeautifulSoap 解析HTML文档并抽取文本
1.  jieba 分词
1.  sk-learn 计算TFIDF值
1.  pandas 其他数据处理


```py
def extract_post_content(file):
    soup = BeautifulSoup(open(file).read(), "html.parser")
    return soup.find('div', attrs={'class': 'entry-content'}).text

def extract_all_text():
    with open('filepaths') as f:
        content = f.readlines()

    file_list = [x.strip() for x in content]
    return map(extract_post_content, file_list)

def extract_segments(data):
    seg_list = jieba.cut(data, cut_all=False)
    return [seg.strip() for seg in seg_list if len(seg) > 1]


def tfidf_calc():        
    corpus = [" ".join(item) for item in map(extract_segments, extract_all_text())]

tfidf_calc()
```

`extract_post_content`函数用来打开一篇博客的HTML文件，并提取其中的`div.entry-content`中的文本内容。`extract_all_text`函数用来对文件`filepaths`中的每一行（一篇洞见文章的本地文件路径）都调用一次`extract_post_content`。而函数`extract_segments`会使用`jieba`来对每篇文章进行分词，并生成一个单词组成给的列表。最后，在函数`tfidf_calc`中，通过一个列表推导式来生成语料库。

有了语料库之后，很容易使用`sk-learn`来进行计算：

```py
def tfidf_calc():        
    corpus = [" ".join(item) for item in map(extract_segments, extract_all_text())]
    
    with open('stopwords-utf8.txt') as f:
        content = f.readlines()

    content.extend(['来说', '事情', '提供', '带来', '发现'])
    stopwords = [x.strip().decode('utf-8') for x in content]

    vectorizer = TfidfVectorizer(min_df=1, smooth_idf=False, sublinear_tf=True, stop_words=stopwords)
    vectorizer.fit_transform(corpus)
```

当然，由于处理的是中文，我们需要提供`停止词`来避免对无意义的词的统计（`这个`，`那个`，`然后`等等基本上每篇都会出现多次的词）。在经过`transform`之后，我们就得到了一个稀疏矩阵和词汇表，以及对应的tdidf的值，我们使用`pandas`提供的DataFrame来进行排序和存储即可：

```py
def tfidf_calc(): 
	
	#...

    data = dict(zip(vectorizer.get_feature_names(), vectorizer.idf_))
    result = DataFrame(data.items(), columns=['word', 'tfidf']).sort_values(by='tfidf', ascending=True).head(50)

    result.to_csv('top-50-words-in-tw-insight.csv')
```

```
index,word,tfidf
15809,分享,1.06875559542
5228,方式,1.37439147148
8815,时间,1.39884256735
5128,工作,1.40380535669
21799,过程,1.47066830192
4225,开发,1.48675443967
12707,项目,1.49217450714
10527,技术,1.49762411191
20900,简单,1.49762411191
18756,团队,1.59512247639
...
```

### 可视化

#### 单词云

```js
d3.csv('top-16-words-in-tw-insight.csv', function(err, data) {
    data.forEach(function(d) {
        d.tfidf = +d.tfidf
    });

    d3.layout.cloud().size([1600, 900])
        .words(data)
        .rotate(0)
        .fontSize(function(d) { return Math.round(54/(d.tfidf-1)); })
        .on("end", draw)
        .start();

});
```

这里我直接使用了一个第三方的单词云插件`d3.layout.cloud`，提供一个callback函数`draw`，当布局结束之后，插件会调用这个回调：

```js
function draw(words) {
    d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("class", "wordcloud")
        .append("g")
        .attr("transform", "translate(" + width/2 + "," + height/2 +")")
        .selectAll("text")
        .data(words)
        .enter().append("text")
        .style("font-size", function(d) { return Math.round(54/(d.tfidf-1)) + "px"; })
        .style("fill", function(d, i) { return color(i); })
        .attr("transform", function(d) {
            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function(d) { return d.word; });
}
```

#### 背景图制作

```sh
mkdir -p authors/ && cp wp-content/authors/* authors/
cd authors
mogrify -format png *.jpg 
rm *.jpg
```

将作者的头像制作成一张9x6的大`蒙太奇`图：

```sh
montage *.png  -geometry +0+0 -resize 128x128^ -gravity center -crop 128x128+0+0 -tile 9x6 \
	tw-insight-authors.png
```

#### 后期处理


