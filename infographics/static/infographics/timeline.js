let timeFrame = 'day';
let wSolar = false;

updateTimeLine(timeFrame);

document.getElementById("daySwitch").addEventListener('click', function (timeFrame) {
    timeFrame = 'day';
    updateTimeLine(timeFrame);
});
document.getElementById("weekSwitch").addEventListener('click', function (timeFrame) {
    timeFrame = 'week';
    updateTimeLine(timeFrame);
});
document.getElementById("monthSwitch").addEventListener('click', function (timeFrame) {
    timeFrame = 'month';
    updateTimeLine(timeFrame);
});

function responsivefy(svg) {
    let container = d3.select(svg.node().parentNode),
        width = parseInt(svg.style("width")),
        height = parseInt(svg.style("height")),
        aspect = width / height;
    svg.attr("viewBox", "0 0 " + width + " " + height)
        .attr("preserveAspectRatio", "xMinYMid")
        .call(resize);
    d3.select(window).on("resize." + container.attr("id"), resize);
    function resize() {
        let targetWidth = parseInt(container.style("width"));
        svg.attr("width", targetWidth);
        svg.attr("height", Math.round(targetWidth / aspect));
    }
}

function noSolarBarChart(svg, data, width, height, maxY, xScale, yScale) {
    svg.selectAll('rect')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', 'consumption-rect')
        .attr('x', d => xScale(d.timestamp))
        .attr('y', d => yScale(d.consumption))
        .attr('width', d => width / data.length - 2)
        .attr('height', d => d.consumption * height / maxY);
}

function SolarBarChart(svg, data, width, height, maxY, xScale, yScale) {

// make a stacked chart http://www.adeveloperdiary.com/d3-js/create-stacked-bar-chart-using-d3-js/

    svg.selectAll('rect')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', 'consumption-rect')
        .attr('x', d => xScale(d.timestamp))
        .attr('y', d => yScale(d.consumption))
        .attr('width', d => width / data.length - 2)
        .attr('height', d => d.consumption * height / maxY);
}

function lineChart(svg, data, xScale, yScale) {
    let line = d3.line()
        .x(d => xScale(d.timestamp))
        .y(d => yScale(d.value));

    svg.append('path')
        .data(data['production'])
        .enter()
        .attr('class', 'line')
        .attr("fill", "none")
        .attr('d', d => line(d))
        .attr('stroke', '#efe79c')
        .attr('stroke-width', 4);
}

function parseData(data) {
    let isoParse = d3.timeParse("%Y-%m-%dT%H:%M:%S+00:00Z");

    let process = function (d) {
        d.timestamp = isoParse(d.timestamp);
    };

    data.forEach(process);

    return data;
}


function updateTimeLine(timeFrame, wSolar) {

    $.getJSON('/timeline-update/', {'timeFrame': timeFrame}, function (data, jqXHR) {
        // clean existing chart
        document.getElementById('timeline-chart').innerHTML = '';

        data = parseData(data);

        let t = '%d.%m';
        if (timeFrame == 'day') t = '%H:00';
        let formatTime = d3.timeFormat(t);

// DEBUG
        let out = document.getElementById('formatted');
        out.innerHTML = JSON.stringify(data);
//
        let margin = {top: 10, right: 20, bottom: 60, left: 30};
        let width = 400 - margin.left - margin.right;
        let height = 200 - margin.top - margin.bottom;
        let svg = d3.select('#timeline-chart')
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .call(responsivefy)
            .append('g')
            .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');

        let maxC = d3.max(data.map(d => d.consumption));
        let maxP = d3.max(data.map(d => d.production));
        let maxY = Math.max(maxC, maxP);

        let yScale = d3.scaleLinear()
            .domain([0, maxY])
            .range([height, 0]);
        let yAxis = d3.axisLeft(yScale);

        let xScale = d3.scaleTime()
            .domain(d3.extent(data.map(d => d.timestamp)))
            .range([0, width]);
        let xAxis = d3.axisBottom(xScale)
            .ticks(5)
            .tickSize(4)
            .tickPadding(5)
            .tickFormat(formatTime);

        let z = d3.scaleOrdinal()
            .range(["#F8F6E8", "#56EDA8"]);

        svg.call(yAxis)
            .append('g')
            .attr('transform', `translate(0, ${height})`)
            .call(xAxis);

        if (wSolar == false) noSolarBarChart(svg, data, width, height, maxY, xScale, yScale);
        else SolarBarChart(svg, data, width, height, maxY, xScale, yScale);
        //lineChart(svg, data, xScale, yScale);

    });
}
