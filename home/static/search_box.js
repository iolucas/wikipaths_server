

function SearchBox(initialText) {
    var self = this;
    
    var searchDiv = d3.select(document.body)
        .append("div")
        // .style("background-color", "black")
        .style("position", "relative")
        .style("z-index", 10000);

    var tableRow = searchDiv
        .append("table")
        .style("width", "100%")
        .style("background-color", "#fff")
        .style("margin-bottom", "10px")
        // .style("height", "80px")
        .append("tr")
        // .style("border", "2px solid #000")
        // .style("width", "100%")
        .style("height", "40px");
        

    tableRow.append("td")
        .style("padding-left", "10px")
        .append("input")
        .attr("id", "search-input")
        .attr("autocomplete","off")
        .attr("type", "text")
        // .style("display", "inline-block")
        .style("width", "100%")
        .style("border", 0)
        .attr("value", initialText)
        .attr("placeholder", "Search something...")
        .on("input", function() {
            if(this.value.trim())
                self.search(this.value.trim());
            else 
                self.clear();
        });

    //Append clear button
    tableRow.append("td")
        .attr("id", "search-clear-but")
        .style("cursor", "pointer")
        // .style("background-color", "#aaa")
        // .style("vertical-align", "center")
        .style("border-left", "1px solid #555")
        .style("width", "40px")
        .style("text-align", "center")
        .style("font-size", "20px")
        .style("font-weight", "bold")
        .style("color", "#555")
        .style("visibility", "collapse")
        .text("X")
        .on("click", function() {
            self.clear();
        });


    // var inputDiv = searchDiv.append("div")
    //     

    //     .style("background-color", "#fff")
    //     .style("padding", "10px");

    // inputDiv.append("input")
    //     .attr("type", "text")
    //     .style("display", "inline-block")
    //     .style("width", "100%")
    //     .style("border", 0)
    //     .attr("value", initialText)
    //     .attr("placeholder", "Search something...")
    //     .on("input", function() {
    //         // console.log(this.value);
    //         self.search(this.value);
    //     });

    // inputDiv.append("div")
    //     .style("display", "inline-block")
    //     .style("width", "20px")
    //     .style("height", "20px")
    //     .style("background-color", "yellow");

    // searchDiv.append("span").text("testesteste")
    
    // var searchDiv = d3.select(document.body)
    //     .append("div")
    //     .attr("id", "search-div");
        
    // var formDOM = searchDiv.append("form")
    //     // .attr("actions", "")
    //     // .attr("method", "get")
    //     .style("padding", "10px")
    //     .style("margin-bottom", "10px")

    // formDOM.append("input")
    //     .attr("type", "text")
    //     .attr("name", "page")
    //     .style("width", "100%")
    //     .style("border", 0)
    //     .attr("value", "")
    //     .attr("placeholder", "Search something")
    //     .on("input", function() {
    //         // console.log(this.value);
    //         self.search(this.value);
    //     });

    // formDOM.append("input")
    //     .attr("type", "submit")
    //     .attr("value", "Search");

    this.clear = function() {
        searchDiv.selectAll(".search-result")
            .remove()

        self.hideClearBut();

        d3.select("#search-input").node().value = "";
    }

    this.showClearBut = function() {
        d3.select("#search-clear-but").style("visibility", "visible");
    }

    this.hideClearBut = function() {
        d3.select("#search-clear-but").style("visibility", "collapse");
    }

    this.search = function(searchStr) {
        var searchUrl = "search?q=" + encodeURIComponent(searchStr);
        // var timestamp = new Date().getDate();
        self.showClearBut();

        d3.json(searchUrl, function(data) {

            searchDiv.selectAll(".search-result")
                .remove()
            
            searchDiv.selectAll(".search-result")
                .data(data)
                .enter()
                .append("a")
                .attr("class", "search-result")
                .style("text-decoration", "none")
                .style("color", "#333")
                .attr("href", function(d) { return "?page=" + encodeURIComponent(d[0]); })
                .append("div")
                .style("height", "30px")
                .style("padding", "10px")
                .style("line-height", "30px")
                .style("border-top", "1px solid #777")
                .style("background-color", "#fff")
                .text(function(d) { return d[0]; });
        });
    }
}

