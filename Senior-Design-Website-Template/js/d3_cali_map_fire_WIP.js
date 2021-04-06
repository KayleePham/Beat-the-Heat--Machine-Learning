// Special thanks to http://duspviz.mit.edu/d3-workshop/mapping-data-with-d3/ for the detailed
// tutorial on D3

//  Global variable used for the slider
var inputValue = null;
var year = ["2013","2014","2015","2016","2017","2018", "2019", "2020"];

function run_d3 () {


    // Width and Height of the whole visualization
    var width = innerWidth-40,
        height = innerHeight-40,
        div = d3.select("#incidents").append("div")
        .style("position", "relative");

    // Create SVG
    var svg = d3.select( "body" )
        .append( "svg" )
        .attr( "width", width )
        .attr( "height", height );

    // Append empty placeholder g element to the SVG
    // g will contain geometry elements
    var g = svg.append( "g" );

    // Width and Height of the whole visualization
    // Set Projection Parameters
    var MercProjection = d3.geoMercator() 
        .scale(3000)
        .rotate( [-6,0] )
        .center( [-120, 37] )
        .translate( [width/2,height/2] );

    // Create GeoPath function that uses built-in D3 functionality to turn
    // lat/lon coordinates into screen coordinates
    var geoPath = d3.geoPath()
                    .projection( MercProjection );

    
    //  Populates the empty geometry elements with dataset values for the counties
    g.selectAll( "path" )
        .data( neighborhoods_json.features )
        .enter()
        .append( "path" )
        .attr( "fill", "#ccc" )
        .attr( "stroke", "#333")
        .attr( "d", geoPath );


    
    var incidents = svg.append( "g" );

    //  Populates the empty geometry elements with dataset values for the fires
    incidents.selectAll( "path" )
        .data( fires_json.features )
        .enter()
        .append( "path" )
        .attr( "fill", initialDate )
        .attr( "stroke", "#ccc" )
        .attr( "d", geoPath )
        .attr( "class", "incident")
        .on("mouseover", function(d){
            d3.select("h8").text("Name of fire: " + d.properties.Name + " and acres burned: " + d.properties.AcresBurned);
            d3.select(this).attr("class","incident hover");
        })
        .on("mouseout", function(d){
            d3.select("h8").text("");
            d3.select(this).attr("class","incident");
        });

    // Update function is called when the slider is changed
    d3.select("#timeslide").on("input", function() {
        update(+this.value);
    });

    //  Fills the related data points on the visualization
    function update(value) {
        document.getElementById("range").innerHTML=year[value];
        inputValue = year[value];
        d3.selectAll(".incident")
            .attr("fill", dateMatch);
    }
    
    //  Checks if the dates are matching and appends it according to date
    function dateMatch(data, value) {
        var d = new Date(data.properties.StartedDateOnly);
        var index = d.getFullYear() - 2013;
        var y = year[index];
        if (inputValue == y) {
            this.parentElement.appendChild(this);
            return "red";
        } else {
            return "#999";
        };
    }

    //  Sets the initial date (state) of the visualization
    function initialDate(d,i){
        var d = new Date(d.properties.StartedDateOnly);
        var index = d.getFullYear() - 2013;
        var y = year[index];
        
        if (y == "2013") {
            this.parentElement.appendChild(this);
            return "red";
        } else {
            return "#999";
        };
    }
}

window.onload = run_d3;