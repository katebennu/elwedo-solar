let timeFrame = 'day';
let buildingOn = false;

updateTimeLine(timeFrame, buildingOn);

document.getElementById("daySwitch").addEventListener('click', function (timeFrame) {
    $('#daySwitch').removeClass('time-control-off').addClass('time-control-on');
    $('#weekSwitch').removeClass('time-control-on').addClass('time-control-off');
    $('#monthSwitch').removeClass('time-control-on').addClass('time-control-off');
    timeFrame = 'day';
    updateTimeLine(timeFrame, buildingOn);

});
document.getElementById("weekSwitch").addEventListener('click', function (timeFrame) {
    $('#weekSwitch').removeClass('time-control-off').addClass('time-control-on');
    $('#daySwitch').removeClass('time-control-on').addClass('time-control-off');
    $('#monthSwitch').removeClass('time-control-on').addClass('time-control-off');
    timeFrame = 'week';
    updateTimeLine(timeFrame, buildingOn);
});
document.getElementById("monthSwitch").addEventListener('click', function (timeFrame) {
    $('#monthSwitch').removeClass('time-control-off').addClass('time-control-on');
    $('#weekSwitch').removeClass('time-control-on').addClass('time-control-off');
    $('#daySwitch').removeClass('time-control-on').addClass('time-control-off');
    timeFrame = 'month';
    updateTimeLine(timeFrame, buildingOn);
});


document.getElementById('building-switch').addEventListener('click', function (e) {
    if (buildingOn == false) {
        buildingOn = true;
        $('#building-switch').removeClass('graph-control-off').addClass('graph-control-on');
    }
    else if (buildingOn == true) {
        buildingOn = false;
        $('#building-switch').removeClass('graph-control-on').addClass('graph-control-off');
    }
    updateTimeLine(timeFrame, buildingOn);
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

function drawAxes(data) {
    // time format for X axis
    let t = '%d.%m';
    if (timeFrame == 'day') t = '%H:00';
    let formatTime = d3.timeFormat(t);

    /*        let stack = d3.stack()
     .keys(['savings', 'consumptionLessSavings'])
     .order(d3.stackOrderNone)
     .offset(d3.stackOffsetNone);

     let series = stack(data);*/


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

    // let maxC = d3.max(data.map(d => d.consumption));
    // let maxP = d3.max(data.map(d => d.production));
    // let maxY = Math.max(maxC, maxP);

    let maxY = d3.max(data.map(function (d) {
        if (buildingOn == true) return d.b_consumption;
        else return d.a_consumption;
    }));

    let y = d3.scaleLinear()
        .domain([0, maxY])
        .range([height, 0]);
    let yAxis = d3.axisLeft(y);

    let x = d3.scaleTime()
        .domain(d3.extent(data.map(d => d.timestamp)))
        .range([0, width]);
    let xAxis = d3.axisBottom(x)
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

    return [svg, xAxis, yAxis, width, height, maxY, x, y];
}

function BarChart(svg, data, width, height, maxY, x, y) {
    svg.selectAll('rect')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', 'consumption-rect')
        .attr('x', d => x(d.timestamp))
        .attr('y', function (d) {
            if (buildingOn == true) return y(d.b_consumption);
            else return y(d.a_consumption);
        })

        .attr('width', d => width / data.length - 2)
        .attr('height', function (d) {
            if (buildingOn == true) return d.b_consumption * height / maxY;
            else return d.a_consumption * height / maxY;
        })
}

function color(n) {
    let colors = ['#56EDA8', '#F4F1E4'];
    return colors[n];
}

function stackedBarChart(d3, svg, data, width, height, maxY, x, y) {

// make a stacked chart http://www.adeveloperdiary.com/d3-js/create-stacked-bar-chart-using-d3-js/

    /*    let dataIntermediate = ['savings', 'consumptionLessSavings'].map(function (key) {
     return data.map(function (d) {
     return {x: d['timestamp'], y: d[key]};
     });
     });

     let dataStackLayout = d3.stack()(dataIntermediate);*/

    let stack = d3.stack()
        .keys(['savings', 'consumptionLessSavings'])
        .order(d3.stackOrderNone)
        .offset(d3.stackOffsetNone);

    let series = stack(data);

    let layer = svg.selectAll('.stack')
        .data(series)
        .enter().append('g')
        .attr('class', 'stack')
        .style('fill', (d, i) => color(i));

    layer.selectAll('rect')
        .data(d => d)
        .enter().append('rect')
        .attr('x', d => x(d.x))
        .attr('y', d => y(d.y + d.y0))
        .attr('width', d => width / data.length - 2)
        .attr('height', d => y(d.y0) - y(d.y + d.y0));
}

function parseData(data) {
    let isoParse = d3.timeParse("%Y-%m-%dT%H:%M:%S+00:00Z");
    let process = function (d) {
        d.timestamp = isoParse(d.timestamp);
    };
    data.forEach(process);
    return data;
}


function dataTotal(data) {
    let consumptionTotal = 0, productionTotal = 0, savingsTotal = 0, earningsTotal = 0;
    for (let i = 0; i < data.length; i++) {
        consumptionTotal += data[i]['a_consumption'];
        productionTotal += data[i]['a_production'];
        savingsTotal += data[i]['a_savings'];
        earningsTotal += data[i]['a_earnings'];
    }
    return {
        'consumptionTotal': consumptionTotal,
        'productionTotal': productionTotal,
        'savingsTotal': savingsTotal,
        'earningsTotal': earningsTotal
    };
}

function CO2Chart() {
    let svg = document.getElementById('CO2-chart').appendChild('svg');
    svg.appendChild('circle');


//     <svg width="100" height="100">
//   <circle cx="20" cy="20" r="20" fill="green" />
//   <circle cx="70" cy="70" r="20" fill="purple" />
//      </svg>
}

function carSection(totals) {
    let timeSpan = '';
    if (timeFrame == 'month') timeSpan = 'THIS MONTH';
    else if (timeFrame == 'day') timeSpan = 'TODAY';
    else if (timeFrame == 'week') timeSpan = 'THIS WEEK';
    document.getElementById('produced-text').innerHTML = timeSpan;
    document.getElementById('produced-number').innerHTML = Math.floor(totals['productionTotal']);
}

function updateTimeLine(timeFrame, buildingOn) {

    $.getJSON('/timeline-update/', {'timeFrame': timeFrame}, function (data, jqXHR) {
        // clean existing chart
        document.getElementById('timeline-chart').innerHTML = '';

// DEBUG
        let out = document.getElementById('formatted');
        // out.innerHTML = JSON.stringify(buildingOn);
        // console.log(JSON.stringify(buildingOn));
        //out.innerHTML = buildingOn;
        //console.log(buildingOn);
//

        data = parseData(data);
        let totals = dataTotal(data);

        // update header
        document.getElementById('updated').innerHTML = d3.timeFormat('%d/%m/%y')(data[data.length - 1]['timestamp']);

        let [svg, xAxis, yAxis, width, height, maxY, x, y] = drawAxes(data);

        /*if (wSolar == false) */
        BarChart(svg, data, width, height, maxY, x, y);

        //CO2Chart(data);

        // update car section
        carSection(totals);
    });
}
