var data = {{ context_data|safe }};

    var margin = {top: 10, right: 20, bottom: 60, left: 30};
    var width = 400 - margin.left - margin.right;
    var height = 200 - margin.top - margin.bottom;


    var svg = d3.select('.timeline-chart')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .call(responsivefy)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');

    var formatTime = d3.timeFormat('%H');
    var isoParse = d3.timeParse("%Y-%m-%dT%H:%M:%S+00:00Z");

    data.forEach(function (d) {
        d.timestamp = formatTime(isoParse(d.timestamp));
        d.value = +d.value;
    });

    var maxY = d3.max(data.map(function (d) { return d.value; }))

/*//DEBUG
    var out = document.getElementById('formatted');
    out.innerHTML = JSON.stringify(data);
//DEBUG{*/

    var yScale = d3.scaleLinear()
        .domain([0, maxY])
        .range([height, 0]);
    var yAxis = d3.axisLeft(yScale);
    svg.call(yAxis);

    var domainData = {{ context_data|safe }};

    var xScale = d3.scaleBand()
        .padding(0.2)
        .domain(data.map(d => d.timestamp))
        .range([0, width]);

    var xAxis = d3.axisBottom(xScale)
        .ticks(data.length)
        .tickSize(10)
        .tickPadding(5)

    svg
        .append('g')
        .attr('transform', `translate(0, ${height})`)
        .call(xAxis);


    svg.selectAll('rect')
        .data(data)
        .enter()
        .append('rect')
        .attr('x', d => d.timestamp * width / data.length + 2)
        .attr('y', d => height - d.value * height / maxY)
        .attr('width', d => width / data.length - 2)
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