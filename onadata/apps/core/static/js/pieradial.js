// Uncomment to style it like Apple Watch

if (!Highcharts.theme) {
    Highcharts.setOptions({
        chart: {
            backgroundColor: 'white'
        },
        colors: ['#FFDA83', '#FF6565', '#56D9FE'],
        title: {
            style: {
                color: 'silver'
            }
        },
        tooltip: {
            style: {
                color: 'silver'
            }
        }
    });
}


/**
 * In the chart render event, add icons on top of the circular shapes
 */
function renderIcons() {}

Highcharts.chart('radial-chart', {

    chart: {
        type: 'solidgauge',
        height: '110%',
        events: {
            render: renderIcons
        }
    },

    tooltip: {
        borderWidth: 0,
        backgroundColor: 'none',
        shadow: false,
        style: {
            fontSize: '10px'
        },
        valueSuffix: '%',
        pointFormat: '{series.name}<br><span style="font-size:1.5em; color: {point.color}; font-weight: bold">{point.y}</span>',
        positioner: function (labelWidth) {
            return {
                x: (this.chart.chartWidth - labelWidth) / 2,
                y: (this.chart.plotHeight / 2) + 15
            };
        }
    },

    pane: {
        startAngle: 0,
        endAngle: 360,
        background: [{ // Track for  Post Construction Stage   
            outerRadius: '112%',
            innerRadius: '98%',
            backgroundColor: Highcharts.color(Highcharts.getOptions().colors[0])
                .setOpacity(0.3)
                .get(),
            borderWidth: 0
        }, { // Track for Physical Construction Stage
            outerRadius: '87%',
            innerRadius: '73%',
            backgroundColor: Highcharts.color(Highcharts.getOptions().colors[1])
                .setOpacity(0.3)
                .get(),
            borderWidth: 0
        }, { // Track for Pre-Construction Stage
            outerRadius: '62%',
            innerRadius: '48%',
            backgroundColor: Highcharts.color(Highcharts.getOptions().colors[2])
                .setOpacity(0.3)
                .get(),
            borderWidth: 0
        }]
    },

    yAxis: {
        min: 0,
        max: 100,
        lineWidth: 0,
        tickPositions: []
    },

    plotOptions: {
        solidgauge: {
            dataLabels: {
                enabled: false
            },
            linecap: 'round',
            stickyTracking: false,
            rounded: true
        }
    },

    series: [{
        name: 'Post Construction Stage',
        data: [{
            color: Highcharts.getOptions().colors[0],
            radius: '112%',
            innerRadius: '98%',
            y: 65
        }]
    }, {
        name: 'Physical Construction Stage',
        data: [{
            color: Highcharts.getOptions().colors[1],
            radius: '87%',
            innerRadius: '73%',
            y: 55
        }]
    }, {
        name: 'Pre-Construction Stage',
        data: [{
            color: Highcharts.getOptions().colors[2],
            radius: '62%',
            innerRadius: '48%',
            y: 30
        }]
    }]
});

Highcharts.chart('radial-chart-infoleft', {

    chart: {
        type: 'solidgauge',
        height: '110%',
        events: {
            render: renderIcons
        }
    },

    tooltip: {
        borderWidth: 0,
        backgroundColor: 'none',
        shadow: false,
        style: {
            fontSize: '10px'
        },
        valueSuffix: '%',
        pointFormat: '{series.name}<br><span style="font-size:1.5em; color: {point.color}; font-weight: bold">{point.y}</span>',
        positioner: function (labelWidth) {
            return {
                x: (this.chart.chartWidth - labelWidth) / 2,
                y: (this.chart.plotHeight / 2) + 15
            };
        }
    },

    pane: {
        startAngle: 0,
        endAngle: 360,
        background: [{ // Track for  Post Construction Stage   
            outerRadius: '112%',
            innerRadius: '98%',
            backgroundColor: Highcharts.color(Highcharts.getOptions().colors[0])
                .setOpacity(0.3)
                .get(),
            borderWidth: 0
        }, { // Track for Physical Construction Stage
            outerRadius: '87%',
            innerRadius: '73%',
            backgroundColor: Highcharts.color(Highcharts.getOptions().colors[1])
                .setOpacity(0.3)
                .get(),
            borderWidth: 0
        }, { // Track for Pre-Construction Stage
            outerRadius: '62%',
            innerRadius: '48%',
            backgroundColor: Highcharts.color(Highcharts.getOptions().colors[2])
                .setOpacity(0.3)
                .get(),
            borderWidth: 0
        }]
    },

    yAxis: {
        min: 0,
        max: 100,
        lineWidth: 0,
        tickPositions: []
    },

    plotOptions: {
        solidgauge: {
            dataLabels: {
                enabled: false
            },
            linecap: 'round',
            stickyTracking: false,
            rounded: true
        }
    },

    series: [{
        name: 'Post Construction Stage',
        data: [{
            color: Highcharts.getOptions().colors[0],
            radius: '112%',
            innerRadius: '98%',
            y: 65
        }]
    }, {
        name: 'Physical Construction Stage',
        data: [{
            color: Highcharts.getOptions().colors[1],
            radius: '87%',
            innerRadius: '73%',
            y: 55
        }]
    }, {
        name: 'Pre-Construction Stage',
        data: [{
            color: Highcharts.getOptions().colors[2],
            radius: '62%',
            innerRadius: '48%',
            y: 30
        }]
    }]
});

Highcharts.chart('radial-chart-inforight', {

    chart: {
        type: 'solidgauge',
        height: '110%',
        events: {
            render: renderIcons
        }
    },

    tooltip: {
        borderWidth: 0,
        backgroundColor: 'none',
        shadow: false,
        style: {
            fontSize: '10px'
        },
        valueSuffix: '%',
        pointFormat: '{series.name}<br><span style="font-size:1.5em; color: {point.color}; font-weight: bold">{point.y}</span>',
        positioner: function (labelWidth) {
            return {
                x: (this.chart.chartWidth - labelWidth) / 2,
                y: (this.chart.plotHeight / 2) + 15
            };
        }
    },

    pane: {
        startAngle: 0,
        endAngle: 360,
        background: [{ // Track for  Post Construction Stage   
            outerRadius: '112%',
            innerRadius: '98%',
            backgroundColor: Highcharts.color(Highcharts.getOptions().colors[0])
                .setOpacity(0.3)
                .get(),
            borderWidth: 0
        }, { // Track for Physical Construction Stage
            outerRadius: '87%',
            innerRadius: '73%',
            backgroundColor: Highcharts.color(Highcharts.getOptions().colors[1])
                .setOpacity(0.3)
                .get(),
            borderWidth: 0
        }, { // Track for Pre-Construction Stage
            outerRadius: '62%',
            innerRadius: '48%',
            backgroundColor: Highcharts.color(Highcharts.getOptions().colors[2])
                .setOpacity(0.3)
                .get(),
            borderWidth: 0
        }]
    },

    yAxis: {
        min: 0,
        max: 100,
        lineWidth: 0,
        tickPositions: []
    },

    plotOptions: {
        solidgauge: {
            dataLabels: {
                enabled: false
            },
            linecap: 'round',
            stickyTracking: false,
            rounded: true
        }
    },

    series: [{
        name: 'Post Construction Stage',
        data: [{
            color: Highcharts.getOptions().colors[0],
            radius: '112%',
            innerRadius: '98%',
            y: 65
        }]
    }, {
        name: 'Physical Construction Stage',
        data: [{
            color: Highcharts.getOptions().colors[1],
            radius: '87%',
            innerRadius: '73%',
            y: 55
        }]
    }, {
        name: 'Pre-Construction Stage',
        data: [{
            color: Highcharts.getOptions().colors[2],
            radius: '62%',
            innerRadius: '48%',
            y: 30
        }]
    }]
});