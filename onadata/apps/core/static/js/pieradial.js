// Uncomment to style it like Apple Watch

if (!Highcharts.theme) {
    Highcharts.setOptions({
        chart: {
            backgroundColor: 'white'
        },
        colors: ['#56D9FE', '#FF6565', '#FFDA83'],
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


$(document).ready(function(){
    $.ajax({
        url: '/core/get-phase-data/',
        type: 'GET',
        dataType: 'json',        

        success: function(result){
            $("#radialloader").css("display", "none");  
            var myseries = [];
            var radius = ["110%", "80%", "50%"];
            var inner_radius = ["90%", "60%", "30%"];
            i = 0;
            $("#phases-legend").empty();
            var total = 0;
            $.each (result, function(key, value){
                total = total + value.percentage;
            })
            $.each (result, function(key, value){
                var percentage_value = (value.percentage / total) * 100;
                myseries.push({
                    name: key,
                    data: [{
                        color: Highcharts.getOptions().colors[i],
                        radius: radius[i],
                        innerRadius: inner_radius[i],
                        y: percentage_value,
                    }]
                })
                i += 1;
                $("#phases-legend").append('<li class="legend-data"><label class="body-span-reg">'+ key +'</label><span class="span-numdata"> ('+ percentage_value +'%)</span></li>')
            });   
            act_group_chart = Highcharts.chart('radial-chart', {

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
                        outerRadius: '110%',
                        innerRadius: '90%',
                        backgroundColor: Highcharts.color(Highcharts.getOptions().colors[0])
                            .setOpacity(0.3)
                            .get(),
                        borderWidth: 0
                    }, { // Track for Physical Construction Stage
                        outerRadius: '80%',
                        innerRadius: '60%',
                        backgroundColor: Highcharts.color(Highcharts.getOptions().colors[1])
                            .setOpacity(0.3)
                            .get(),
                        borderWidth: 0
                    }, { // Track for Pre-Construction Stage
                        outerRadius: '50%',
                        innerRadius: '30%',
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
                series: myseries
            });  
            
            var myseries = [];   
            var radius = ["110%", "80%", "50%"];
            var inner_radius = ["90%", "60%", "30%"];
            district.forEach(function(request){
                $.ajax({
                    url: '/core/get-phase-data/',
                    type: 'GET',
                    dataType: 'json',
                    data: {'district': request.id},            
            
                    success: function(result){
                        $("#district-"+request.id+"-loader").css("display", "none");
                        i = 0;
                        $("#district_"+ request.id +"_legend").empty();
                        var total = 0;
                        $.each (result, function(key, value){
                            total = total + value.percentage;
                        })
                        
                        $.each (result, function(key, value){
                            var percentage_value = (value.percentage / total) * 100;
                            myseries.push({
                                name: key,
                                data: [{
                                    color: Highcharts.getOptions().colors[i],
                                    radius: radius[i],
                                    innerRadius: inner_radius[i],
                                    y: percentage_value,
                                }]
                            })
                            i += 1;
                            $("#district_"+ request.id +"_legend").append('<li class="legend-data"><label class="body-span-reg">'+ key +'</label><span class="span-numdata"> ('+ percentage_value +'%)</span></li>')
                        });   
                        chart_div = 'district-'+ request.id +'-radial-chart'
                        Highcharts.chart(chart_div, {
        
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
                                    outerRadius: '110%',
                                    innerRadius: '90%',
                                    backgroundColor: Highcharts.color(Highcharts.getOptions().colors[0])
                                        .setOpacity(0.3)
                                        .get(),
                                    borderWidth: 0
                                }, { // Track for Physical Construction Stage
                                    outerRadius: '80%',
                                    innerRadius: '60%',
                                    backgroundColor: Highcharts.color(Highcharts.getOptions().colors[1])
                                        .setOpacity(0.3)
                                        .get(),
                                    borderWidth: 0
                                }, { // Track for Pre-Construction Stage
                                    outerRadius: '50%',
                                    innerRadius: '30%',
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
                            series: myseries
                        });
                    }
                });  
            });
        }
    });
})
            

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