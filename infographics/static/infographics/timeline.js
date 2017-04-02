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
    let consumptionTotal = 0, productionTotal = 0, consumptionLessSavingsTotal = 0, savingsTotal = 0;
    for (let i = 0; i < data.length; i++) {
        consumptionTotal += data[i]['a_consumption'];
        consumptionLessSavingsTotal += data[i]['a_consumptionLessSavings'];
        productionTotal += data[i]['a_production'];
        savingsTotal += data[i]['a_savings'];
    }

    return [Math.floor(savingsTotal / consumptionTotal * 100),
        [{'value': consumptionTotal, title: 'consumptionTotal'},
            {'value': consumptionLessSavingsTotal, title: 'consumptionLessSavingsTotal'}],
        productionTotal];
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


function euroChart(data) {
    let margin = {top: 5, right: 5, bottom: 0, left: 5};
    let width = 190 - margin.left - margin.right;
    let height = 185 - margin.top - margin.bottom;
    let svg = d3.select('#euro-chart')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');

    let maxY = d3.max(data.map(d => d.value));

    let y = d3.scaleLinear()
        .domain([0, maxY])
        .range([height, 0]);

    let x = d3.scaleBand()
        .padding(0.5)
        .domain(data.map(d => d.title))
        .range([0, width]);
    let xAxis = d3.axisBottom(x);

    let color = d3.scaleOrdinal().range(["#56eda8", "26B5DB"]);

    svg.selectAll('rect')
        .data(data)
        .enter()
        .append('rect')
        .attr('fill', 'blue')
        .attr('x', d => x(d.title) - 5)
        .attr('y', d => y(d.value))
        .attr('width', '50px')
        .attr('height', d => height - y(d.value))
        .style('fill', ((d, i) => color(i)));

    svg.append('line')
        .attr('x1', 0)
        .attr('y1', 181)
        .attr('x2', 180)
        .attr('y2', 181)
        .style('stroke', '#6D6A5C')
        .style('stroke-width', '2');

}

function donutChart(savingsRate) {
    let o = 0, n = 50, x = savingsRate, m = 50 - x;
    if (x > 50) {o = x - 50; n = 50 - o; x = 50; m = 0}

    let data = [o, n, 100 + x, m];

    let width = 215,
        height = 380,
        radius = 115;

    let color = d3.scaleOrdinal()
        .range(["#26B5DB", "#F4F1E4", "#26B5DB", "#F4F1E4"]);

    let arc = d3.arc()
        .outerRadius(radius - 10)
        .innerRadius(60);

    let pie = d3.pie()
        .sort(null)
        .value(function (d) {
            return d;
        });

    let svg = d3.select("#donut-chart").append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    svg.append('line')
        .attr('x1', -100)
        .attr('y1', -2)
        .attr('x2', 180)
        .attr('y2', -2)
        .style('stroke', '#6D6A5C')
        .style('stroke-width', '2');


    let g = svg.selectAll(".arc")
        .data(pie(data))
        .enter().append("g")
        .attr("class", "arc");

    g.append("path")
        .attr("d", arc)
        .style("fill", function (d) {
            return color(d.data);
        });


}

function CO2Chart() {


}

function carSection(productionTotal, timeFrame) {
    let timeSpan = '';
    if (timeFrame == 'month') timeSpan = 'THIS MONTH';
    else if (timeFrame == 'day') timeSpan = 'TODAY';
    else if (timeFrame == 'week') timeSpan = 'THIS WEEK';
    document.getElementById('produced-text').innerHTML = timeSpan;
    document.getElementById('produced-number').innerHTML = String(Math.floor(productionTotal));
    document.getElementById('produced-km').innerHTML = String(Math.floor(productionTotal) * 5);
}

function updateTimeLine(timeFrame, buildingOn, savingsOn) {

    $.getJSON('/timeline-update/', {'timeFrame': timeFrame}, function (data, jqXHR) {
        // clean existing chart
        document.getElementById('timeline-chart').innerHTML = '';
        document.getElementById('euro-chart').innerHTML = '';
        document.getElementById('donut-chart').innerHTML = '';


        data = parseData(data);

        let [savingsRate, totals, productionTotal] = getDataTotal(data);


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
        console.log(savingsRate);
//

        donutChart(savingsRate);

        euroChart(totals);
        //CO2Chart(data);

        // update car section
        carSection(productionTotal, timeFrame);
    });
    return [timeFrame, buildingOn]
}
