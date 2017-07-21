

function SearchBox(initialText) {
    var self = this;

    var searchDiv = d3.select("#search-area")
        .append("div")
        // .style("background-color", "black")
        .style("position", "relative")
        .style("z-index", 10000);

    var tableRow = searchDiv
        .append("table")
        .style("width", "100%")
        .style("background-color", "#fff")
        // .style("margin-bottom", "10px")
        // .style("height", "80px")
        .append("tr")
        // .style("border", "2px solid #000")
        // .style("width", "100%")
        .style("height", "50px");
        
    var changeTimeoutToken = null;

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

            clearTimeout(changeTimeoutToken);

            var searchInputValue = this.value.trim();

            if(searchInputValue) {
                changeTimeoutToken = setTimeout(function() {
                    // console.log(searchInputValue)
                    self.search(searchInputValue);
                }, 300);
            } else {
                self.clear();
            }


        });

    //Append clear button
    tableRow.append("td")
        .attr("id", "search-clear-but")
        .style("cursor", "pointer")
        // .style("background-color", "#aaa")
        // .style("vertical-align", "center")
        .style("border-left", "1px solid #555")
        .style("width", "50px")
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

    if(initialText)
        this.showClearBut();

    this.hideClearBut = function() {
        d3.select("#search-clear-but").style("visibility", "collapse");
    }

    this.search = function(searchStr) {
        //Ensures late queries overlap the screen with the search box empty
        if(d3.select("#search-input").node().value == "") {
            self.clear();
            return;
        }

        var searchUrl = "/search?q=" + encodeURIComponent(searchStr);
        // var timestamp = new Date().getDate();
        self.showClearBut();

        d3.json(searchUrl, function(data) {

            searchDiv.selectAll(".search-result")
                .remove()
            
            // searchDiv.append("div")
            //     .attr("class", "search-result")
            //     .style("background-color", "#ddd")
            //     .style("height", "10px");

            var searchRes = searchDiv.selectAll(".search-result")
                .data(data)
                .enter()
                .append("a")
                .attr("class", "search-result")
                .style("text-decoration", "none")
                .style("color", "#333")
                .attr("href", function(d) { return "/map/" + encodeURIComponent(d[0]); })
                .append("div")
                // .style("height", "30px")
                .style("padding", "5px 5px 5px 10px")
                // .style("line-height", "30px")
                .style("border-top", "1px solid #777")
                .style("background-color", "#f1f1f1");

            searchRes.append("span")
                // .style("margin", "0")
                // .style("padding", "0")
                // .style("line-height", 0)
                .style("font-size", "15px")
                .style("font-weight", "bold")
                .text(function(d) { return d[0]; });

            searchRes.append("br");

            searchRes.append("span")
                // .style("margin", "0")
                // .style("padding", "0")
                // .style("line-height", 0)
                .text(function(d) { 
                    if(d[1].length > 80)
                        return d[1].substring(0, 80) + "...";
                    return d[1]
                })
        });
    }
}

