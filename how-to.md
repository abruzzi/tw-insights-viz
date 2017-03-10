
```sh
wget --mirror -p --html-extension --convert-links -e robots=off -P . http://insights.thoughtworkers.org/
```

```sh
mkdir insights
find insights.thoughtworkers.org/ -name index.html -depth 2 > filepaths
```

