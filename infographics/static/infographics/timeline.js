
//TODO: change /day/ to a virable obtained from day/week/month switch
$.getJSON('/timeline-update/', function(data, jqXHR) {
    var d = JSON.stringify(data);


var out = document.getElementById('formatted');
out.innerHTML = JSON.stringify(data['production']);

// BAR CHART
    var margin = {top: 10, right: 20, bottom: 60, left: 30};
    var width = 400 - margin.left - margin.right;
    var height = 200 - margin.top - margin.bottom;
    var svg = d3.select('#timeline-chart')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .call(responsivefy)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');

// PARSE DATA
    var formatTime = d3.timeFormat('%H');
    var isoParse = d3.timeParse("%Y-%m-%dT%H:%M:%S+00:00Z");

    var consumption = data['consumption'].forEach(function (d) {
        d.timestamp = isoParse(d.timestamp);
        d.value = +d.value;
    });
    var production = data['production'].forEach(function (d) {
        d.timestamp = isoParse(d.timestamp);
        d.value = +d.value;
    });

//TODO: get max from both consumption and production
    var maxY = d3.max(consumption.map(d => d.value));

    var yScale = d3.scaleLinear()
        .domain([0, maxY])
        .range([height, 0]);
    var yAxis = d3.axisLeft(yScale);
    svg.call(yAxis);

    var xScale = d3.scaleTime()
        .domain(d3.extent(consumption.map(d =>d.timestamp)))
        .range([0, width]);
    var xAxis = d3.axisBottom(xScale)
        //.ticks(data['consumption'].length)
        .tickSize(10)
        .tickPadding(5)
    svg
        .append('g')
        .attr('transform', `translate(0, ${height})`)
        .call(xAxis);
    svg.selectAll('rect')
        .data(consumption)
        .enter()
        .append('rect')
        .attr('x', d => formatTime(d.timestamp) * width / consumption.length + 2)
        .attr('y', d => height - d.value * height / maxY)
        .attr('width', d => width / consumption.length - 2)
        .attr('height', d => d.value * height / maxY);




// LINE CHART
    var line = d3.line()
    .x(d => formatTime((d.timestamp)) * width / d.length + 2)
    .y(d => height - d.value * height / maxY);

    svg.selectAll('line')
        .data(production)
        .enter()
        .append('path')
        .attr('class', 'line')
        .attr("fill", "none")
        .attr('d', d => line(d))  // REPLACE values
        .style('stroke', '#efe79c')
        .style('stroke-width', 4)



    function responsivefy(svg) {
        var container = d3.select(svg.node().parentNode),
            width = parseInt(svg.style("width")),
            height = parseInt(svg.style("height")),
            aspect = width / height;
        svg.attr("viewBox", "0 0 " + width + " " + height)
            .attr("preserveAspectRatio", "xMinYMid")
            .call(resize);
        d3.select(window).on("resize." + container.attr("id"), resize);
        function resize() {
            var targetWidth = parseInt(container.style("width"));
            svg.attr("width", targetWidth);
            svg.attr("height", Math.round(targetWidth / aspect));
        }
    }

});