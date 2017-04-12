let timeFrame = 'day';
let buildingOn = false;
let savingsOn = true;

updateTimeLine(timeFrame = 'day', buildingOn = false);
updateWeather();

// stick the timeFrame switching div to the top
$(window).scroll(function () {
    let anchor = $('#sticky-anchor'),
        ribbon = $('#sticky-ribbon'),
        windowTop = $(window).scrollTop(),
        divTop = $(anchor).offset().top;
    if (windowTop > divTop) {
        $(ribbon).addClass('stick');
        $(anchor).css('display', 'block');
    } else {
        $(ribbon).removeClass('stick');
        $(anchor).css('display', 'block');
    }
});

// small graphs - change view from one line to a carousel
$(window).on('resize load', function () {
    if ($(window).width() < 1000) {
        slide(ids);
    } else {
        $('.slide').removeClass('hidden');
        $('.arrow').addClass('hidden');
    }
});

// data preparation
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
    let savingsRate = Math.round(savingsTotal / consumptionTotal * 100);


    return [savingsRate,
        [{'value': consumptionTotal, title: 'consumptionTotal'},
            {'value': consumptionLessSavingsTotal, title: 'consumptionLessSavingsTotal'}],
        productionTotal,
        [consumptionTotal, consumptionLessSavingsTotal]];
}

function updateHeader(data) {
    let updated = data[data.length - 1]['timestamp'];
    if (timeFrame != 'day') updated = updated.setDate(updated.getDate() + 1);
    document.getElementById('updated').innerHTML = d3.timeFormat('%d/%m/%y')(updated);

}

// timeline description pop-up
// $('#timeline-heading').click(function () {
//     $("#timeline-popup").addClass("show");
//
// //     $('body').click(function() {
// //     if (!$(this.target).is('#timeline-popup')){
// //        $("#timeline-popup").removeClass("show");
// //     }
// // });
// });
// $('#timeline-popup-close').click(function () {
//     $("#timeline-popup").removeClass("show");
// });


$("#timeline-heading").click(function (e) {
    e.preventDefault();
    $("#timeline-popup").fadeIn(300,function(){$(this).focus();});
});

$('#timeline-popup-close').click(function () {
    $("#timeline-popup").fadeOut();
});

$('#timeline-popup').on('blur', function () {
        $("#timeline-popup").fadeOut(300);
});


// switch timeFrame
$("#daySwitch").click(function () {
    $('#daySwitch').removeClass('time-control-off').addClass('time-control-on');
    $('#weekSwitch').removeClass('time-control-on').addClass('time-control-off');
    $('#monthSwitch').removeClass('time-control-on').addClass('time-control-off');
    timeFrame = 'day';
    updateTimeLine(timeFrame, buildingOn, savingsOn);

});
$("#weekSwitch").click(function () {
    $('#weekSwitch').removeClass('time-control-off').addClass('time-control-on');
    $('#daySwitch').removeClass('time-control-on').addClass('time-control-off');
    $('#monthSwitch').removeClass('time-control-on').addClass('time-control-off');
    timeFrame = 'week';
    updateTimeLine(timeFrame, buildingOn, savingsOn);
});
$("#monthSwitch").click(function () {
    $('#monthSwitch').removeClass('time-control-off').addClass('time-control-on');
    $('#weekSwitch').removeClass('time-control-on').addClass('time-control-off');
    $('#daySwitch').removeClass('time-control-on').addClass('time-control-off');
    timeFrame = 'month';
    updateTimeLine(timeFrame, buildingOn, savingsOn);
});

// timeline
$('#building-switch').click(function () {
    if (buildingOn == false) {
        buildingOn = true;
        $('#building-switch').removeClass('graph-control-off').addClass('graph-control-on');

    }
    else if (buildingOn == true) {
        buildingOn = false;
        $('#building-switch').removeClass('graph-control-on').addClass('graph-control-off');
    }
    console.log(timeFrame, buildingOn, savingsOn);

//// Update only timeline graph instead
    updateTimeLine(timeFrame, buildingOn, savingsOn);
});
$('#savings-switch').click(function () {
    if (savingsOn == false) {
        savingsOn = true;
        $('#savings-switch').removeClass('graph-control-off').addClass('graph-control-on');

    }
    else if (savingsOn == true) {
        savingsOn = false;
        $('#savings-switch').removeClass('graph-control-on').addClass('graph-control-off');
    }
    console.log(timeFrame, buildingOn, savingsOn);

    //// Update only timeline graph instead
    updateTimeLine(timeFrame, buildingOn, savingsOn);
});

function drawAxes(data, timeFrame, buildingOn) {
    // time format for X axis
    let t = '%d.%m.';
    if (timeFrame == 'day') t = '%H:%M';
    let formatTime = d3.timeFormat(t);

    let margin = {top: 10, right: 10, bottom: 60, left: 30};
    let width = 700 - margin.left - margin.right;
    let height = 350 - margin.top - margin.bottom;
    let svg = d3.select('#timeline-chart')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        //.call(responsivefy)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');

    let maxY = d3.max(data.map(function (d) {
        if (buildingOn == true) return d.b_consumption;
        else return d.a_consumption;
    }));

    let y = d3.scaleLinear()
        .domain([0, maxY])
        .range([height, 0]);
    let yAxis = d3.axisLeft(y)
        .ticks(5)
        .tickSize(-width)
        .tickFormat(d3.format(",.2f"));

    let x = d3.scaleBand()
        .padding(0.2)
        .domain(data.map(d => d.timestamp))
        .range([0, width]);
    let xAxis = d3.axisBottom(x)
        .ticks(3)
        .tickSize(4)
        .tickPadding(5)
        .tickFormat(formatTime)
        .tickSizeOuter(0)
        .tickValues(x.domain().filter((d, i) => {
            if (timeFrame == 'week') return !(i % 2);
            else return !(i % 5);
        }));

    svg.append('g')
        .attr("class", "axisY")
        .style('font-size', '8px')
        .style('stroke-width', '1px')
        .call(yAxis);


    return [svg, xAxis, yAxis, width, height, maxY, x, y];
}
function appendXAxis(svg, height, xAxis) {
    svg.append('g')
        .attr('transform', `translate(0, ${height})`)
        .attr("class", "axisX")
        .style('font-size', '8px')
        .call(xAxis);
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

        .attr('width', d => x.bandwidth())
        .attr('height', function (d) {
            if (buildingOn == true) return height - y(d.b_consumption);
            else return height - y(d.a_consumption);
        })
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

    let keys = ['consumptionLessSavings', 'savings'];
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
        .attr("width", d => x.bandwidth());


    return data;
}

// small charts
function euroChart(data) {
    let margin = {top: 20, right: 5, bottom: 0, left: 5};
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
        .attr('y1', 166)
        .attr('x2', 180)
        .attr('y2', 166)
        .style('stroke', '#6D6A5C')
        .style('stroke-width', '2');

    let wS = (data[0]['value'] * 8 / 100).toFixed(1);
    if (wS >= 10) wS = Math.round(data[0]['value'] * 8 / 100);

    let wSHeight = $("#euro-chart rect:first-of-type").height();

    svg.append("text")
        .attr('x', 45)
        .attr('y', -8 + height - wSHeight) // + height - height of the first rect
        .attr('fill', '#56eda8')
        .attr('font-size', 16)
        .attr('font-weight', 'bold')
        .text(wS + ' €');

    let wOS = (data[1]['value'] * 8 / 100).toFixed(1);
    if (wOS >= 10) wOS = Math.round(data[1]['value'] * 8 / 100);

    let wSOHeight = $("#euro-chart rect:nth-of-type(2)").height();


    svg.append("text")
        .attr('x', 113)
        .attr('y', -8 + height - wSOHeight) // + height - height of the first rect
        .attr('fill', '#26B5DB')
        .attr('font-size', 16)
        .attr('font-weight', 'bold')
        .text(wOS + ' €');

}
function donutChart(savingsRate) {
    let o = 0, n = 50, x = savingsRate, m = 50 - x;
    if (x > 50) {
        o = x - 50;
        n = 50 - o;
        x = 50;
        m = 0
    }

    let data = [o, n, 100 + x, m];

    let width = 220,
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

    let g = svg.selectAll(".arc")
        .data(pie(data))
        .enter().append("g")
        .attr("class", "arc");

    g.append("path")
        .attr("d", arc)
        .style("fill", function (d) {
            return color(d.data);
        });

    svg.append("text")
        .attr('x', -15)
        .attr('y', -18)
        .attr('fill', '#26B5DB')
        .attr('font-size', 16)
        .attr('font-weight', 'bold')
        .text(savingsRate + ' %');

    svg.append('line')
        .attr('x1', -130)
        .attr('y1', -1)
        .attr('x2', 190)
        .attr('y2', -1)
        .style('stroke', '#6D6A5C')
        .style('stroke-width', '2');


}
function CO2Chart(data) {

    let consumptionTotal = data[0];
    let consumptionLessSavingsTotal = data[1];

    let consumptionRate = Math.round(consumptionTotal / (consumptionTotal + consumptionLessSavingsTotal) * 100);
    let consumptionLessSavingsRate = 100 - consumptionRate;

    $('#green-circle').attr("r", String(consumptionRate * 0.75));
    $('#blue-circle').attr("r", String(consumptionLessSavingsRate * 0.75));

    $('#co2-wO').text(Math.round(data[0] * 209 / 100));
    $('#co2-w').text(Math.round(data[1] * 209 / 100));
}

let ids = ['#slide1', '#slide2', '#slide3'];
function slide(ids) {
    $(ids[0]).removeClass('hidden');
    $('.arrow').removeClass('hidden');
    $(ids[1]).addClass('hidden');
    $(ids[2]).addClass('hidden');
    return ids;
}
function leftArrow(ids) {
    let first = ids.pop();
    ids.unshift(first);
    slide(ids);
    return ids;
}
function rightArrow(ids) {
    let last = ids.shift();
    ids.push(last);
    slide(ids);
    return ids;
}

// weather section
function updateWeather() {
    let iconCodes = {
        '01d': '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<svg width=\"96px\" height=\"96px\" viewBox=\"0 0 96 96\" version=\"1.1\" xmlns=\"http:\/\/www.w3.org\/2000\/svg\" xmlns:xlink=\"http:\/\/www.w3.org\/1999\/xlink\">\r\n    <title>clear sky<\/title>\r\n    <desc>Created with Sketch.<\/desc>\r\n    <defs><\/defs>\r\n    <g id=\"Welcome\" stroke=\"none\" stroke-width=\"1\" fill=\"none\" fill-rule=\"evenodd\">\r\n        <g id=\"Weather\" transform=\"translate(-44.000000, -101.000000)\" fill=\"#EFE79C\">\r\n            <g id=\"Weather-Section\" transform=\"translate(-2.000000, -8.000000)\">\r\n                <g id=\"clear-sky\" transform=\"translate(46.000000, 109.000000)\">\r\n                    <circle id=\"Sun\" cx=\"48\" cy=\"48\" r=\"48\"><\/circle>\r\n                <\/g>\r\n            <\/g>\r\n        <\/g>\r\n    <\/g>\r\n<\/svg>',
        '02d': '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<svg width=\"139px\" height=\"96px\" viewBox=\"0 0 139 96\" version=\"1.1\" xmlns=\"http:\/\/www.w3.org\/2000\/svg\" xmlns:xlink=\"http:\/\/www.w3.org\/1999\/xlink\">\r\n    <!-- Generator: Sketch 41 (35326) - http:\/\/www.bohemiancoding.com\/sketch -->\r\n    <title>few clouds<\/title>\r\n    <desc>Created with Sketch.<\/desc>\r\n    <defs><\/defs>\r\n    <g id=\"Welcome\" stroke=\"none\" stroke-width=\"1\" fill=\"none\" fill-rule=\"evenodd\">\r\n        <g id=\"Weather\" transform=\"translate(-183.000000, -101.000000)\">\r\n            <g id=\"Weather-Section\" transform=\"translate(-2.000000, -8.000000)\">\r\n                <g id=\"few-clouds\" transform=\"translate(185.000000, 109.000000)\">\r\n                    <g id=\"Sun-Cloudy\">\r\n                        <circle id=\"Sun\" fill=\"#EFE79C\" cx=\"69\" cy=\"48\" r=\"48\"><\/circle>\r\n                        <g id=\"Couldy3\" transform=\"translate(0.000000, 15.000000)\" fill=\"#FFFFFF\">\r\n                            <path d=\"M0,65.5024373 L113.620392,65.5024373 C113.620392,65.5024373 110.231134,52.3131982 92.0254388,56.9148746 C77.4385817,37.076667 53.3007055,46.8814388 53.3007055,46.8814388 C51.0124105,40.6817081 33.3849952,31.4593149 20.7400648,49.2357745 C5.86123068,48.4996793 0,65.5024373 0,65.5024373 Z\" id=\"Cloud\"><\/path>\r\n                            <path d=\"M60.8497854,18.2678571 L138.851809,18.2678571 C138.851809,18.2678571 136.525034,9.213256 124.026565,12.3723726 C114.012479,-1.24684048 97.4414817,5.48427553 97.4414817,5.48427553 C95.8705344,1.22807174 83.7690618,-5.10323302 75.0881364,7.10056061 C64.8736041,6.59522076 60.8497854,18.2678571 60.8497854,18.2678571 Z\" id=\"Cloud-2\" transform=\"translate(99.850797, 9.133929) scale(-1, 1) translate(-99.850797, -9.133929) \"><\/path>\r\n                        <\/g>\r\n                    <\/g>\r\n                <\/g>\r\n            <\/g>\r\n        <\/g>\r\n    <\/g>\r\n<\/svg>',
        '03d': '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<svg width=\"139px\" height=\"66px\" viewBox=\"0 0 139 66\" version=\"1.1\" xmlns=\"http:\/\/www.w3.org\/2000\/svg\" xmlns:xlink=\"http:\/\/www.w3.org\/1999\/xlink\">\r\n    <!-- Generator: Sketch 41 (35326) - http:\/\/www.bohemiancoding.com\/sketch -->\r\n    <title>scattered clouds<\/title>\r\n    <desc>Created with Sketch.<\/desc>\r\n    <defs><\/defs>\r\n    <g id=\"Welcome\" stroke=\"none\" stroke-width=\"1\" fill=\"none\" fill-rule=\"evenodd\">\r\n        <g id=\"Weather\" transform=\"translate(-377.000000, -116.000000)\" fill=\"#FFFFFF\">\r\n            <g id=\"Weather-Section\" transform=\"translate(-2.000000, -8.000000)\">\r\n                <g id=\"scattered-clouds\" transform=\"translate(379.000000, 124.000000)\">\r\n                    <g id=\"Cloudy\">\r\n                        <path d=\"M0,65.5024373 L113.620392,65.5024373 C113.620392,65.5024373 110.231134,52.3131982 92.0254388,56.9148746 C77.4385817,37.076667 53.3007055,46.8814388 53.3007055,46.8814388 C51.0124105,40.6817081 33.3849952,31.4593149 20.7400648,49.2357745 C5.86123068,48.4996793 0,65.5024373 0,65.5024373 Z\" id=\"Cloud\"><\/path>\r\n                        <path d=\"M60.8497854,18.2678571 L138.851809,18.2678571 C138.851809,18.2678571 136.525034,9.213256 124.026565,12.3723726 C114.012479,-1.24684048 97.4414817,5.48427553 97.4414817,5.48427553 C95.8705344,1.22807174 83.7690618,-5.10323302 75.0881364,7.10056061 C64.8736041,6.59522076 60.8497854,18.2678571 60.8497854,18.2678571 Z\" id=\"Cloud-2\" transform=\"translate(99.850797, 9.133929) scale(-1, 1) translate(-99.850797, -9.133929) \"><\/path>\r\n                    <\/g>\r\n                <\/g>\r\n            <\/g>\r\n        <\/g>\r\n    <\/g>\r\n<\/svg>',
        '04d': '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<svg width=\"140px\" height=\"96px\" viewBox=\"0 0 140 96\" version=\"1.1\" xmlns=\"http:\/\/www.w3.org\/2000\/svg\" xmlns:xlink=\"http:\/\/www.w3.org\/1999\/xlink\">\r\n    <!-- Generator: Sketch 41 (35326) - http:\/\/www.bohemiancoding.com\/sketch -->\r\n    <title>broken clouds<\/title>\r\n    <desc>Created with Sketch.<\/desc>\r\n    <defs><\/defs>\r\n    <g id=\"Welcome\" stroke=\"none\" stroke-width=\"1\" fill=\"none\" fill-rule=\"evenodd\">\r\n        <g id=\"Weather\" transform=\"translate(-596.000000, -101.000000)\" fill=\"#FFFFFF\">\r\n            <g id=\"Weather-Section\" transform=\"translate(-2.000000, -8.000000)\">\r\n                <g id=\"broken-clouds\" transform=\"translate(598.000000, 109.000000)\">\r\n                    <g id=\"Cloudy\">\r\n                        <path d=\"M61.8497854,18.2678571 L139.851809,18.2678571 C139.851809,18.2678571 137.525034,9.213256 125.026565,12.3723726 C115.012479,-1.24684048 98.4414817,5.48427553 98.4414817,5.48427553 C96.8705344,1.22807174 84.7690618,-5.10323302 76.0881364,7.10056061 C65.8736041,6.59522076 61.8497854,18.2678571 61.8497854,18.2678571 Z\" id=\"Cloud-2\" transform=\"translate(100.850797, 9.133929) scale(-1, 1) translate(-100.850797, -9.133929) \"><\/path>\r\n                        <path d=\"M1,63.1976472 L138,63.1976472 C138,63.1976472 139.967697,38.7655302 111.961464,44.1612296 C94.3730776,18.6658997 65.2683633,31.2666294 65.2683633,31.2666294 C62.5092071,23.298965 41.2546079,11.4466867 26.0077369,34.2923344 C-1.20170574,34.2923344 1,63.1976472 1,63.1976472 Z\" id=\"Cloud\"><\/path>\r\n                        <path d=\"M13,95.5024373 L126.620392,95.5024373 C126.620392,95.5024373 123.231134,82.3131982 105.025439,86.9148746 C90.4385817,67.076667 66.3007055,76.8814388 66.3007055,76.8814388 C64.0124105,70.6817081 46.3849952,61.4593149 33.7400648,79.2357745 C18.8612307,78.4996793 13,95.5024373 13,95.5024373 Z\" id=\"Cloud\" transform=\"translate(69.810196, 82.197647) scale(-1, 1) translate(-69.810196, -82.197647) \"><\/path>\r\n                    <\/g>\r\n                <\/g>\r\n            <\/g>\r\n        <\/g>\r\n    <\/g>\r\n<\/svg>',
        '09d': '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<svg width=\"114px\" height=\"78px\" viewBox=\"0 0 114 78\" version=\"1.1\" xmlns=\"http:\/\/www.w3.org\/2000\/svg\" xmlns:xlink=\"http:\/\/www.w3.org\/1999\/xlink\">\r\n    <!-- Generator: Sketch 41 (35326) - http:\/\/www.bohemiancoding.com\/sketch -->\r\n    <title>shower rain<\/title>\r\n    <desc>Created with Sketch.<\/desc>\r\n    <defs><\/defs>\r\n    <g id=\"Welcome\" stroke=\"none\" stroke-width=\"1\" fill=\"none\" fill-rule=\"evenodd\">\r\n        <g id=\"Weather\" transform=\"translate(-964.000000, -109.000000)\">\r\n            <g id=\"Weather-Section\" transform=\"translate(-2.000000, -8.000000)\">\r\n                <g id=\"shower-rain\" transform=\"translate(966.000000, 117.000000)\">\r\n                    <g id=\"Cloudy\">\r\n                        <path d=\"M102,67 L108.596219,75.5804227\" id=\"Path-2\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                        <path d=\"M85,64 L91.596219,72.5804227\" id=\"Path-2-Copy\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                        <path d=\"M44,64 L50.596219,72.5804227\" id=\"Path-2-Copy-5\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                        <path d=\"M82,43 L88.596219,51.5804227\" id=\"Path-2\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                        <path d=\"M65,40 L71.596219,48.5804227\" id=\"Path-2-Copy\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                        <path d=\"M60,56 L66.596219,64.5804227\" id=\"Path-2-Copy-2\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                        <path d=\"M43,37 L49.596219,45.5804227\" id=\"Path-2-Copy-3\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                        <path d=\"M24,40 L30.596219,48.5804227\" id=\"Path-2-Copy-5\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                        <path d=\"M0,26.6095801 L113.620392,26.6095801 C113.620392,26.6095801 110.231134,13.4203411 92.0254388,18.0220174 C77.4385817,-1.81619011 53.3007055,7.98858168 53.3007055,7.98858168 C51.0124105,1.78885094 33.3849952,-7.43354225 20.7400648,10.3429173 C5.86123068,9.60682218 0,26.6095801 0,26.6095801 Z\" id=\"Cloud\" fill=\"#FFFFFF\"><\/path>\r\n                    <\/g>\r\n                <\/g>\r\n            <\/g>\r\n        <\/g>\r\n    <\/g>\r\n<\/svg>',
        '10d': '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<svg width=\"138px\" height=\"97px\" viewBox=\"0 0 138 97\" version=\"1.1\" xmlns=\"http:\/\/www.w3.org\/2000\/svg\" xmlns:xlink=\"http:\/\/www.w3.org\/1999\/xlink\">\r\n    <!-- Generator: Sketch 41 (35326) - http:\/\/www.bohemiancoding.com\/sketch -->\r\n    <title>rain<\/title>\r\n    <desc>Created with Sketch.<\/desc>\r\n    <defs><\/defs>\r\n    <g id=\"Welcome\" stroke=\"none\" stroke-width=\"1\" fill=\"none\" fill-rule=\"evenodd\">\r\n        <g id=\"Weather\" transform=\"translate(-792.000000, -101.000000)\">\r\n            <g id=\"Weather-Section\" transform=\"translate(-2.000000, -8.000000)\">\r\n                <g id=\"rain\" transform=\"translate(794.000000, 109.000000)\">\r\n                    <path d=\"M0.04271795,42.1976472 L137.042718,42.1976472 C137.042718,42.1976472 139.010415,17.7655302 111.004182,23.1612296 C93.4157955,-2.33410029 64.3110813,10.2666294 64.3110813,10.2666294 C61.551925,2.298965 40.2973258,-9.55331329 25.0504548,13.2923344 C-2.15898779,13.2923344 0.04271795,42.1976472 0.04271795,42.1976472 Z\" id=\"Cloud\" fill=\"#FFFFFF\"><\/path>\r\n                    <path d=\"M113.254131,63.3135328 L123.808122,77.0422624\" id=\"Path-2\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M102.725439,74.567275 L113.27943,88.2960046\" id=\"Path-2-Copy\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M87.68445,74.567275 L98.2384413,88.2960046\" id=\"Path-2-Copy-2\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M66.6270656,70.0657781 L77.1810568,83.7945077\" id=\"Path-2-Copy-3\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M59.1065711,81.3195203 L69.6605624,95.0482499\" id=\"Path-2-Copy-4\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M36.5450878,74.567275 L47.0990791,88.2960046\" id=\"Path-2-Copy-5\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M96.7090433,40 L107.263035,53.7287296\" id=\"Path-2\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M86.1803511,51.2537422 L96.7343424,64.9824718\" id=\"Path-2-Copy\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M71.1393622,51.2537422 L81.6933535,64.9824718\" id=\"Path-2-Copy-2\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M50.0819778,46.7522453 L60.6359691,60.4809749\" id=\"Path-2-Copy-3\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M42.5614833,58.0059875 L53.1154746,71.7347171\" id=\"Path-2-Copy-4\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M20,51.2537422 L30.5539913,64.9824718\" id=\"Path-2-Copy-5\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                <\/g>\r\n            <\/g>\r\n        <\/g>\r\n    <\/g>\r\n<\/svg>',
        '11d': '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<svg width=\"138px\" height=\"97px\" viewBox=\"0 0 138 97\" version=\"1.1\" xmlns=\"http:\/\/www.w3.org\/2000\/svg\" xmlns:xlink=\"http:\/\/www.w3.org\/1999\/xlink\">\r\n    <!-- Generator: Sketch 41 (35326) - http:\/\/www.bohemiancoding.com\/sketch -->\r\n    <title>thunderstorm<\/title>\r\n    <desc>Created with Sketch.<\/desc>\r\n    <defs><\/defs>\r\n    <g id=\"Welcome\" stroke=\"none\" stroke-width=\"1\" fill=\"none\" fill-rule=\"evenodd\">\r\n        <g id=\"Weather\" transform=\"translate(-1158.000000, -101.000000)\">\r\n            <g id=\"Weather-Section\" transform=\"translate(-2.000000, -8.000000)\">\r\n                <g id=\"thunderstorm\" transform=\"translate(1160.000000, 109.000000)\">\r\n                    <g id=\"Cloudy\">\r\n                        <path d=\"M0.04271795,42.1976472 L137.042718,42.1976472 C137.042718,42.1976472 139.010415,17.7655302 111.004182,23.1612296 C93.4157955,-2.33410029 64.3110813,10.2666294 64.3110813,10.2666294 C61.551925,2.298965 40.2973258,-9.55331329 25.0504548,13.2923344 C-2.15898779,13.2923344 0.04271795,42.1976472 0.04271795,42.1976472 Z\" id=\"Cloud\" fill=\"#FFFFFF\"><\/path>\r\n                        <path d=\"M113.254131,63.3135328 L123.808122,77.0422624\" id=\"Path-2\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                        <path d=\"M102.725439,74.567275 L113.27943,88.2960046\" id=\"Path-2-Copy\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                        <path d=\"M89.5,77.5 L98.2384413,88.2960046\" id=\"Path-2-Copy-2\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                        <path d=\"M66.6270656,70.0657781 L77.1810568,83.7945077\" id=\"Path-2-Copy-3\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                        <path d=\"M59.1065711,81.3195203 L69.6605624,95.0482499\" id=\"Path-2-Copy-4\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                        <path d=\"M36.5450878,74.567275 L47.0990791,88.2960046\" id=\"Path-2-Copy-5\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                        <path d=\"M96.7090433,40 L107.263035,53.7287296\" id=\"Path-2\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                        <path d=\"M42.5614833,58.0059875 L53.1154746,71.7347171\" id=\"Path-2-Copy-4\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                        <path d=\"M20,51.2537422 L30.5539913,64.9824718\" id=\"Path-2-Copy-5\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <\/g>\r\n                    <polygon id=\"Path-3\" fill=\"#EFE79C\" points=\"67.3479514 34.0920644 44.4754124 33.9570839 59.9278267 53.7060603 80.8155822 52.9246944 91.4086989 66.0463189 83.2680446 41.9171305 72.3840544 41.9551495\"><\/polygon>\r\n                <\/g>\r\n            <\/g>\r\n        <\/g>\r\n    <\/g>\r\n<\/svg>',
        '13d': '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<svg width=\"138px\" height=\"94px\" viewBox=\"0 0 138 94\" version=\"1.1\" xmlns=\"http:\/\/www.w3.org\/2000\/svg\" xmlns:xlink=\"http:\/\/www.w3.org\/1999\/xlink\">\r\n    <!-- Generator: Sketch 41 (35326) - http:\/\/www.bohemiancoding.com\/sketch -->\r\n    <title>snow<\/title>\r\n    <desc>Created with Sketch.<\/desc>\r\n    <defs><\/defs>\r\n    <g id=\"Welcome\" stroke=\"none\" stroke-width=\"1\" fill=\"none\" fill-rule=\"evenodd\">\r\n        <g id=\"Weather\" transform=\"translate(-1348.000000, -101.000000)\">\r\n            <g id=\"Weather-Section\" transform=\"translate(-2.000000, -8.000000)\">\r\n                <g id=\"snow\" transform=\"translate(1350.000000, 109.000000)\">\r\n                    <path d=\"M0.04271795,42.1976472 L137.042718,42.1976472 C137.042718,42.1976472 139.010415,17.7655302 111.004182,23.1612296 C93.4157955,-2.33410029 64.3110813,10.2666294 64.3110813,10.2666294 C61.551925,2.298965 40.2973258,-9.55331329 25.0504548,13.2923344 C-2.15898779,13.2923344 0.04271795,42.1976472 0.04271795,42.1976472 Z\" id=\"Cloud\" fill=\"#FFFFFF\"><\/path>\r\n                    <path d=\"M115.254131,73.3135328 L115.863603,74.1063401\" id=\"Path-2\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M104.725439,84.567275 L105.334911,85.3600823\" id=\"Path-2-Copy\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M89.68445,84.567275 L90.2939224,85.3600823\" id=\"Path-2-Copy-2\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M68.6270656,80.0657781 L69.2365379,80.8585854\" id=\"Path-2-Copy-3\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M61.1065711,91.3195203 L61.7160435,92.1123276\" id=\"Path-2-Copy-4\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M38.5450878,84.567275 L39.1545602,85.3600823\" id=\"Path-2-Copy-5\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M98.7090433,50 L99.3185157,50.7928073\" id=\"Path-2\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M88.1803511,61.2537422 L88.7898235,62.0465495\" id=\"Path-2-Copy\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M73.1393622,61.2537422 L73.7488346,62.0465495\" id=\"Path-2-Copy-2\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M52.0819778,56.7522453 L52.6914502,57.5450526\" id=\"Path-2-Copy-3\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M44.5614833,68.0059875 L45.1709557,68.7987948\" id=\"Path-2-Copy-4\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M22,61.2537422 L22.6094724,62.0465495\" id=\"Path-2-Copy-5\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                <\/g>\r\n            <\/g>\r\n        <\/g>\r\n    <\/g>\r\n<\/svg>',
        '50d': '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<svg width=\"142px\" height=\"88px\" viewBox=\"0 0 142 88\" version=\"1.1\" xmlns=\"http:\/\/www.w3.org\/2000\/svg\" xmlns:xlink=\"http:\/\/www.w3.org\/1999\/xlink\">\r\n    <!-- Generator: Sketch 41 (35326) - http:\/\/www.bohemiancoding.com\/sketch -->\r\n    <title>mist<\/title>\r\n    <desc>Created with Sketch.<\/desc>\r\n    <defs><\/defs>\r\n    <g id=\"Welcome\" stroke=\"none\" stroke-width=\"1\" fill=\"none\" fill-rule=\"evenodd\">\r\n        <g id=\"Weather\" transform=\"translate(-1547.000000, -101.000000)\">\r\n            <g id=\"Weather-Section\" transform=\"translate(-2.000000, -8.000000)\">\r\n                <g id=\"mist\" transform=\"translate(1551.000000, 109.000000)\">\r\n                    <path d=\"M0.04271795,42.1976472 L137.042718,42.1976472 C137.042718,42.1976472 139.010415,17.7655302 111.004182,23.1612296 C93.4157955,-2.33410029 64.3110813,10.2666294 64.3110813,10.2666294 C61.551925,2.298965 40.2973258,-9.55331329 25.0504548,13.2923344 C-2.15898779,13.2923344 0.04271795,42.1976472 0.04271795,42.1976472 Z\" id=\"Cloud\" fill=\"#FFFFFF\"><\/path>\r\n                    <path d=\"M1,51.5 L136.611578,51.5\" id=\"Path-2\" stroke=\"#FFFFFF\" stroke-width=\"5\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M36,62 L69,62\" id=\"Path-2-Copy-6\" stroke=\"#FFFFFF\" stroke-width=\"4\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M82,62 L122,62\" id=\"Path-2-Copy-6\" stroke=\"#FFFFFF\" stroke-width=\"4\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M19.5,75 L130.5,75\" id=\"Path-2-Copy-7\" stroke=\"#FFFFFF\" stroke-width=\"3\" stroke-linecap=\"round\"><\/path>\r\n                    <path d=\"M34,87 L95,87\" id=\"Path-2-Copy-8\" stroke=\"#FFFFFF\" stroke-width=\"2\" stroke-linecap=\"round\"><\/path>\r\n                <\/g>\r\n            <\/g>\r\n        <\/g>\r\n    <\/g>\r\n<\/svg>'
    };
    let days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];

    let url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=Helsinki,FI&cnt=7&appid=cf704fd01f3c91f15bdf00a58b867142'
    $.getJSON(url, function (json) {
        let lst = json['list'];
        for (let i = 1; i < 7; i++) {
            let d = new Date(lst[i]['dt'] * 1000);
            let day = days[d.getDay()];
            let date = String(d.getDate());
            if (date.length == 1) date = '0' + date;
            let month = String(d.getMonth() + 1);
            if (month.length == 1) month = '0' + month;
            let id = '#weather' + i;
            if (i != 1) $(id + '> p').text(day + ' ' + date + '/' + month);

            let weatherCode = lst[i]['weather'][0]['icon'];
            $(id + '> div').html(iconCodes[weatherCode]);

        }
    });
}

// car section
function carSection(productionTotal, timeFrame) {
    let timeSpan = '';
    if (timeFrame == 'month') timeSpan = 'THIS MONTH';
    else if (timeFrame == 'day') timeSpan = 'TODAY';
    else if (timeFrame == 'week') timeSpan = 'THIS WEEK';
    document.getElementById('produced-text').innerHTML = timeSpan;
    document.getElementById('produced-number').innerHTML = String(Math.floor(productionTotal));
    document.getElementById('produced-km').innerHTML = String(Math.floor(productionTotal) * 5);
}


// main
function updateTimeLine(timeFrame, buildingOn, savingsOn) {

    $.getJSON('/timeline-update/', {'timeFrame': timeFrame}, function (data, jqXHR) {
        // clean existing chart
        document.getElementById('timeline-chart').innerHTML = '';
        document.getElementById('euro-chart').innerHTML = '';
        document.getElementById('donut-chart').innerHTML = '';

        parseData(data);
        let [savingsRate, totals, productionTotal, CO2Rates] = getDataTotal(data);

        // update header
        updateHeader(data);
        let latest = data[data.length - 1]['timestamp'];
        if (timeFrame != 'day') latest = latest.setDate(latest.getDate() - 1);

        let [svg, xAxis, yAxis, width, height, maxY, x, y] = drawAxes(data, timeFrame, buildingOn);
        $(".tick > text").filter(function () {
            return $(this).text() === "0.00";
        }).css("display", "none");

        /*if (wSolar == false) */
        if (savingsOn == false) BarChart(svg, data, width, height, maxY, x, y);
        else stackedChart(data, buildingOn, svg, width, height, maxY, x, y);
        appendXAxis(svg, height, xAxis);


// DEBUG
        // let out = document.getElementById('formatted');
        // out.innerHTML = JSON.stringify(buildingOn);
        // console.log(JSON.stringify(data));
        //out.innerHTML = buildingOn;
        // console.log(data);
//

        donutChart(savingsRate);
        euroChart(totals);
        CO2Chart(CO2Rates);

        // update car section
        carSection(productionTotal, timeFrame);
    });
    return [timeFrame, buildingOn]
}
