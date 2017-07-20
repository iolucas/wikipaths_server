var LoadScreen = {}

LoadScreen.show = function() {
    d3.select("#load-screen").remove();

    d3.select("body")
        .append("div")
        .attr("id", "load-screen")
        .style("width", "100%")
        .style("height", "100%")
        .style("background-color", "rgba(0,0,0,0.8)")
        .style("position", "absolute")
        .style("top", 0)
        .style("z-index", 100000)
        .style("text-align", "center")
        .append("span")
        .style("line-height", window.innerHeight + "px")
        .style("font-size", "30px")
        .text("Loading...")
        // .attr("text-anchor", "middle")
        .style("color", "#ddd");
        // .attr("x", "50%")
        // .attr("y", "50%"); 
}

LoadScreen.hide = function() {
    d3.select("#load-screen").remove();
}