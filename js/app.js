window.onload = function() {
    var wca = ["#F4841E", "#9A9A9A", "#9D683E", "#D07624", "#CBCCCB", "#F2C69F"];
    var color = d3.scale.linear()
            .range(wca);

    var grays = ["#ddd", "#ccc", "#bbb", "#aaa", "#999", "#888", "#777", "#666", "#555", "#444", "#333", "#222"];

    var width = 2000,
        height = 1100;

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

    d3.csv('top-16-words-in-tw-insight.csv', function(err, data) {
        data.forEach(function(d) {
            d.tfidf = +d.tfidf
        });

        color.domain(d3.range(data.length));

        d3.layout.cloud().size([1600, 900])
            .words(data)
            .rotate(0)
            .fontSize(function(d) { return Math.round(54/(d.tfidf-1)); })
            .on("end", draw)
            .start();

    });
}