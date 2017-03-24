
//TODO: change /day/ to a virable obtained from day/week/month switch
$.getJSON('/timeline-update/', function(data, jqXHR) {
    var d = JSON.stringify(data);


var out = document.getElementById('formatted');
out.innerHTML = JSON.stringify(data['consumption']);

//var data = {{ context_data|safe }};
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

    var formatTime = d3.timeFormat('%H');
    var isoParse = d3.timeParse("%Y-%m-%dT%H:%M:%S+00:00Z");

//TODO: get max from both consumption and production
    var maxY = d3.max((data['consumption']).map(function (d) { return d['value']; }));

    var yScale = d3.scaleLinear()
        .domain([0, maxY])
        .range([height, 0]);
    var yAxis = d3.axisLeft(yScale);
    svg.call(yAxis);

    var timestamps = function () {

    }

    var xScale = d3.scaleTime()
        .domain(d3.extent(data['consumption'].map(d => isoParse(d.timestamp))))
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
        .data(data['consumption'])
        .enter()
        .append('rect')
        .attr('x', d => formatTime(isoParse(d.timestamp)) * width / data['consumption'].length + 2)
        .attr('y', d => height - d.value * height / maxY)
        .attr('width', d => width / data['consumption'].length - 2)
        .attr('height', d => d.value * height / maxY);
    function responsivefy(svg) {
        // get container + svg aspect ratio
        var container = d3.select(svg.node().parentNode),
            width = parseInt(svg.style("width")),
            height = parseInt(svg.style("height")),
            aspect = width / height;
        // add viewBox and preserveAspectRatio properties,
        // and call resize so that svg resizes on inital page load
        svg.attr("viewBox", "0 0 " + width + " " + height)
            .attr("preserveAspectRatio", "xMinYMid")
            .call(resize);
        // to register multiple listeners for same event type,
        // you need to add namespace, i.e., 'click.foo'
        // necessary if you call invoke this function for multiple svgs
        // api docs: https://github.com/mbostock/d3/wiki/Selections#on
        d3.select(window).on("resize." + container.attr("id"), resize);
        // get width of container and resize svg to fit it
        function resize() {
            var targetWidth = parseInt(container.style("width"));
            svg.attr("width", targetWidth);
            svg.attr("height", Math.round(targetWidth / aspect));
        }
    }

});