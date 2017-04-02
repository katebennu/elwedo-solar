let timeFrame = 'day';
let buildingOn = false;
let savingsOn = true;

updateTimeLine(timeFrame = 'day', buildingOn = false);

document.getElementById("daySwitch").addEventListener('click', function (e) {
    $('#daySwitch').removeClass('time-control-off').addClass('time-control-on');
    $('#weekSwitch').removeClass('time-control-on').addClass('time-control-off');
    $('#monthSwitch').removeClass('time-control-on').addClass('time-control-off');
    timeFrame = 'day';
    updateTimeLine(timeFrame, buildingOn, savingsOn);

});
document.getElementById("weekSwitch").addEventListener('click', function (e) {
    $('#weekSwitch').removeClass('time-control-off').addClass('time-control-on');
    $('#daySwitch').removeClass('time-control-on').addClass('time-control-off');
    $('#monthSwitch').removeClass('time-control-on').addClass('time-control-off');
    timeFrame = 'week';
    updateTimeLine(timeFrame, buildingOn, savingsOn);
});
document.getElementById("monthSwitch").addEventListener('click', function (e) {
    $('#monthSwitch').removeClass('time-control-off').addClass('time-control-on');
    $('#weekSwitch').removeClass('time-control-on').addClass('time-control-off');
    $('#daySwitch').removeClass('time-control-on').addClass('time-control-off');
    timeFrame = 'month';
    updateTimeLine(timeFrame, buildingOn, savingsOn);
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
    console.log(timeFrame, buildingOn, savingsOn);
    updateTimeLine(timeFrame, buildingOn, savingsOn);
});

document.getElementById('savings-switch').addEventListener('click', function (e) {
    if (savingsOn == false) {
        savingsOn = true;
        $('#savings-switch').removeClass('graph-control-off').addClass('graph-control-on');

    }
    else if (savingsOn == true) {
        savingsOn = false;
        $('#savings-switch').removeClass('graph-control-on').addClass('graph-control-off');
    }
    console.log(timeFrame, buildingOn, savingsOn);
    updateTimeLine(timeFrame, buildingOn, savingsOn);
});

function responsivefy(svg, timeFrame) {
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

function drawAxes(data, timeFrame, buildingOn) {
    // time format for X axis
    let t = '%d.%m';
    if (timeFrame == 'day') t = '%H:00';
    let formatTime = d3.timeFormat(t);

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

function parseData(data) {
    let isoParse = d3.timeParse("%Y-%m-%dT%H:%M:%S+00:00Z");
    let process = function (d) {
        d.timestamp = isoParse(d.timestamp);
    };
    data.forEach(process);
    return data;
}

function getDataTotal(data) {
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

function stackedChart(fullData, buildingOn, svg, width, height, maxY, x, y) {
    data = [];
    if (buildingOn == true) {
        for (let i = 0; i < fullData.length; i++) {
            data.push({
                'timestamp': fullData[i]['timestamp'],
                'savings': fullData[i]['b_savings'],
                'consumptionLessSavings': fullData[i]['b_consumptionLessSavings']
            });
        }
    } else {
        for (let i = 0; i < fullData.length; i++) {
            data.push({
                'timestamp': fullData[i]['timestamp'],
                'savings': fullData[i]['a_savings'],
                'consumptionLessSavings': fullData[i]['a_consumptionLessSavings']
            });
        }
    }
    data.push({'columns': ['timestamp', 'savings', 'consumptionLessSavings']});

    let keys = ['savings', 'consumptionLessSavings'];
    let z = d3.scaleOrdinal()
        .range(["#F4F1E4", "#56eda8"]);
    z.domain(keys);

    svg.append("g")
        .selectAll("g")
        .data(d3.stack().keys(keys)(data))
        .enter().append("g")
        .attr("fill", function (d) {
            return z(d.key);
        })
        .selectAll("rect")
        .data(function (d) {
            return d;
        })
        .enter().append("rect")
        .attr("x", function (d) {
            return x(d.data.timestamp);
        })
        .attr("y", function (d) {
            return y(d[1]);
        })
        .attr("height", function (d) {
            return y(d[0]) - y(d[1]);
        })
        .attr("width", d => width / data.length - 2);


    return data;
}


function euroChart(totals) {
    let margin = {top: 10, right: 10, bottom: 10, left: 10};
    let width = 100 - margin.left - margin.right;
    let height = 200 - margin.top - margin.bottom;
    let svg = d3.select('#euro-chart')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .call(responsivefy)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');

    let maxY = d3.max(data.map(d => d.a_consumption));

    let y = d3.scaleLinear()
        .domain([0, maxY])
        .range([height, 0]);
    let yAxis = d3.axisLeft(y)
        .ticks(5)
        .tickSize(4)
        .tickPadding(5);

    let x = d3.scaleOrdinal()
        .domain(d3.extent(data.map(d => d.timestamp)))
        .range([0, width]);
    let xAxis = d3.axisBottom(x)




}


function CO2Chart() {


}

function carSection(totals, timeFrame) {
    let timeSpan = '';
    if (timeFrame == 'month') timeSpan = 'THIS MONTH';
    else if (timeFrame == 'day') timeSpan = 'TODAY';
    else if (timeFrame == 'week') timeSpan = 'THIS WEEK';
    document.getElementById('produced-text').innerHTML = timeSpan;
    document.getElementById('produced-number').innerHTML = Math.floor(totals['productionTotal']);
    document.getElementById('produced-km').innerHTML = Math.floor(totals['productionTotal']) * 5;
}

function updateTimeLine(timeFrame, buildingOn, savingsOn) {

    $.getJSON('/timeline-update/', {'timeFrame': timeFrame}, function (data, jqXHR) {
        // clean existing chart
        document.getElementById('timeline-chart').innerHTML = '';


        data = parseData(data);
        let totals = getDataTotal(data);


        // update header
        document.getElementById('updated').innerHTML = d3.timeFormat('%d/%m/%y')(data[data.length - 1]['timestamp']);

        let [svg, xAxis, yAxis, width, height, maxY, x, y] = drawAxes(data, timeFrame, buildingOn);

        /*if (wSolar == false) */
        if (savingsOn == false) BarChart(svg, data, width, height, maxY, x, y);
        else stackedChart(data, buildingOn, svg, width, height, maxY, x, y);

// DEBUG
        let out = document.getElementById('formatted');
        // out.innerHTML = JSON.stringify(buildingOn);
        //console.log(JSON.stringify(data));
        //out.innerHTML = buildingOn;
        console.log(stackedData);
//

        euroChart(totals);
        //CO2Chart(data);

        // update car section
        carSection(totals, timeFrame);
    });
    return [timeFrame, buildingOn]
}
