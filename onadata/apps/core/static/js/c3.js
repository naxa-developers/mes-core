$(function() {
    "use strict";
    setTimeout(function(){ 
        $(document).ready(function(){
            var chart = c3.generate({
                bindto: '#chart-employment', // id of chart wrapper   
                data: {
                    columns: [
                        // each columns data
                        ['data1', 2, 8, 6, 7, 14, 11],
                        ['data2', 5, 15, 11, 15, 21, 25],
                        ['data3', 17, 18, 21, 20, 30, 29]
                    ],
                    type: 'line', // default type of chart
                    colors: {
                        'data1': "cyan",
                        'data2': "blue",
                        'data3': "green"
                    },
                    names: {
                        // name of each serie
                        'data1': 'Development',
                        'data2': 'Marketing',
                        'data3': 'Sales'
                    }
                },
                axis: {
                    x: {
                        type: 'category',
                        // name of each category
                        categories: ['2013', '2014', '2015', '2016', '2019', '2018']
                    },
                },
                legend: {
                    show: true, //hide legend
                },
                padding: {
                    bottom: 0,
                    top: 0
                },
            });
        });
        $(document).ready(function(){
            var chart = c3.generate({
                bindto: '#cluseter_time', // id of chart wrapper
                data: {
                    columns: [
                        // each columns data
                        ['data1', 6.0, 10, 14, 10],
                        ['data2', 4, 8, 10, 8],
                        ['data3', 1, 4, 6, 4],
                    ],
                    labels: true,
                    type: 'line', // default type of chart
                    colors: {
                        'data1': "#e3e3e3",
                        'data2': "#00A890",
                        'data3': "#0d89df"
                    },
                    names: {
                        // name of each serie
                        'data1': 'Cluster-1',
                        'data2': 'Cluster-2',
                        'data3': 'Cluster-3'
                    }
                },
                axis: {
                    x: {
                        type: 'category',
                        // name of each category
                        categories: ['Q1', 'Q2', 'Q3', 'Q4']
                    },
                },
                legend: {
                    show: true, //hide legend
                },
                padding: {
                    bottom: 0,
                    top: 0
                },
            });
        });
        $(document).ready(function(){
            var chart = c3.generate({
                bindto: '#chart-area', // id of chart wrapper
                data: {
                    columns: [
                        // each columns data
                        ['data1', 11, 8, 15, 18, 19, 17],
                        ['data2', 7, 7, 5, 7, 9, 12]
                    ],
                    type: 'area', // default type of chart
                    colors: {
                        'data1': "blue",
                        'data2': "cyan"
                    },
                    names: {
                        // name of each serie
                        'data1': 'Maximum',
                        'data2': 'Minimum'
                    }
                },
                axis: {
                    x: {
                        type: 'category',
                        // name of each category
                        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
                    },
                },
                legend: {
                    show: true, //hide legend
                },
                padding: {
                    bottom: 0,
                    top: 0
                },
            });
        });
        $(document).ready(function(){
            var chart = c3.generate({
                bindto: '#chart-area-spline', // id of chart wrapper
                data: {
                    columns: [
                        // each columns data
                        ['data1', 11, 8, 15, 18, 19, 17],
                        ['data2', 7, 7, 5, 7, 9, 12]
                    ],
                    type: 'area-spline', // default type of chart
                    colors: {
                        'data1': "blue",
                        'data2': "cyan"
                    },
                    names: {
                        // name of each serie
                        'data1': 'Maximum',
                        'data2': 'Minimum'
                    }
                },
                axis: {
                    x: {
                        type: 'category',
                        // name of each category
                        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
                    },
                },
                legend: {
                    show: true, //hide legend
                },
                padding: {
                    bottom: 0,
                    top: 0
                },
            });
        });
        $(document).ready(function(){
            var chart = c3.generate({
                bindto: '#chart-area-spline-sracked', // id of chart wrapper
                data: {
                    columns: [
                        // each columns data
                        ['data1', 11, 8, 15, 18, 19, 17],
                        ['data2', 7, 7, 5, 7, 9, 12]
                    ],
                    type: 'area-spline', // default type of chart
                    groups: [
                        [ 'data1', 'data2']
                    ],
                    colors: {
                        'data1': "blue",
                        'data2': "cyan"
                    },
                    names: {
                        // name of each serie
                        'data1': 'Maximum',
                        'data2': 'Minimum'
                    }
                },
                axis: {
                    x: {
                        type: 'category',
                        // name of each category
                        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
                    },
                },
                legend: {
                    show: true, //hide legend
                },
                padding: {
                    bottom: 0,
                    top: 0
                },
            });
        });
        $(document).ready(function(){
            var chart = c3.generate({
                bindto: '#chart-spline', // id of chart wrapper
                data: {
                    columns: [
                        // each columns data
                        ['data1', 0.2, 0.8, 0.8, 0.8, 1, 1.3, 1.5, 2.9, 1.9, 2.6, 1.6, 3, 4, 3.6, 4.5, 4.2, 4.5, 4.5, 4, 3.1, 2.7, 4, 2.7, 2.3, 2.3, 4.1, 7.7, 7.1, 5.6, 6.1, 5.8, 8.6, 7.2, 9, 10.9, 11.5, 11.6, 11.1, 12, 12.3, 10.7, 9.4, 9.8, 9.6, 9.8, 9.5, 8.5, 7.4, 7.6],
                        ['data2', 0, 0, 0.6, 0.9, 0.8, 0.2, 0, 0, 0, 0.1, 0.6, 0.7, 0.8, 0.6, 0.2, 0, 0.1, 0.3, 0.3, 0, 0.1, 0, 0, 0, 0.2, 0.1, 0, 0.3, 0, 0.1, 0.2, 0.1, 0.3, 0.3, 0, 3.1, 3.1, 2.5, 1.5, 1.9, 2.1, 1, 2.3, 1.9, 1.2, 0.7, 1.3, 0.4, 0.3]
                    ],
                    labels: true,
                    type: 'spline', // default type of chart
                    colors: {
                        'data1': "blue",
                        'data2': "cyan"
                    },
                    names: {
                        // name of each serie
                        'data1': 'Hestavollane',
                        'data2': 'Vik'
                    }
                },
                axis: {
                    x: {
                        type: 'category',
                        // name of each category
                        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
                    },
                },
                legend: {
                    show: true, //hide legend
                },
                padding: {
                    bottom: 0,
                    top: 0
                },
            });
        });
        $(document).ready(function(){
            var chart = c3.generate({
                bindto: '#chart-spline-rotated', // id of chart wrapper
                data: {
                    columns: [
                        // each columns data
                        ['data1', 11, 8, 15, 18, 19, 17],
                        ['data2', 7, 7, 5, 7, 9, 12]
                    ],
                    type: 'spline', // default type of chart
                    colors: {
                        'data1': "blue",
                        'data2':"cyan"
                    },
                    names: {
                        // name of each serie
                        'data1': 'Maximum',
                        'data2': 'Minimum'
                    }
                },
                axis: {
                    x: {
                        type: 'category',
                        // name of each category
                        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
                    },
                    rotated: true,
                },
                legend: {
                    show: true, //hide legend
                },
                padding: {
                    bottom: 0,
                    top: 0
                },
            });
        });
        $(document).ready(function(){
            var chart = c3.generate({
                bindto: '#chart-step', // id of chart wrapper
                data: {
                    columns: [
                        // each columns data
                        ['data1', 11, 8, 15, 18, 19, 17],
                        ['data2', 7, 7, 5, 7, 9, 12]
                    ],
                    type: 'step', // default type of chart
                    colors: {
                        'data1': "blue",
                        'data2': "cyan"
                    },
                    names: {
                        // name of each serie
                        'data1': 'Maximum',
                        'data2': 'Minimum'
                    }
                },
                axis: {
                    x: {
                        type: 'category',
                        // name of each category
                        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
                    },
                },
                legend: {
                    show: true, //hide legend
                },
                padding: {
                    bottom: 0,
                    top: 0
                },
            });
        });
        $(document).ready(function(){
            var chart = c3.generate({
                bindto: '#chart-area-step', // id of chart wrapper
                data: {
                    columns: [
                        // each columns data
                        ['data1', 11, 8, 15, 18, 19, 17],
                        ['data2', 7, 7, 5, 7, 9, 12]
                    ],
                    type: 'area-step', // default type of chart
                    colors: {
                        'data1': "blue",
                        'data2': "cyan"
                    },
                    names: {
                        // name of each serie
                        'data1': 'Maximum',
                        'data2': 'Minimum'
                    }
                },
                axis: {
                    x: {
                        type: 'category',
                        // name of each category
                        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
                    },
                },
                legend: {
                    show: true, //hide legend
                },
                padding: {
                    bottom: 0,
                    top: 0
                },
            });
        });
        $(document).ready(function(){
            var chart = c3.generate({
                bindto: '#chart-bar', // id of chart wrapper
                data: {
                    columns: [
                        // each columns data
                        ['data1', 100, 200, 300, 250, 350, 150,500,1000,400, 800],
                        ['data2', 200, 150, 600, 350, 250, 300,650, 750, 1200, 1500]
                    ],
                    type: 'bar', // default type of chart
                    
                    colors: {
                        'data1': "#00A890",
                        'data2': "#0d89df"
                    },
                    names: {
                        // name of each serie
                        'data1': 'marginlized',
                        'data2': 'Vulnerable'
                    }
                },
                axis: {
                    x: {
                        type: 'category',
                        // name of each category
                        categories: ['Household awareness creation', 'verification and listing', 'Household awareness creation', 'verification and listing' , 'Household awareness creation', 'verification and listing' , 'Household awareness creation', 'verification and listing' , 'Household awareness creation', 'verification and listing' ],
                        
                    },
                },
                bar: {
                    width: 16
                },
                legend: {
                    show: true, //hide legend
                    position: 'inset',
                    inset: {
                            anchor: 'bottom-right',
                            x: 50,
                            y: -30,
                            step: 1
                        }
                },
                padding: {
                    bottom: 0,
                    top: 30
                },
            });
        });
        $(document).ready(function(){
            var chart = c3.generate({
                bindto: '#chart-bar-rotated', // id of chart wrapper
                data: {
                    columns: [
                        // each columns data
                        ['data1', 11, 8, 15, 18, 19, 17],
                        ['data2', 7, 7, 5, 7, 9, 12],
                        ['data3', 9, 5, 10, 18, 15, 12]
                    ],
                    type: 'bar', // default type of chart
                    colors: {
                        'data1': "#e3e3e3",
                        'data2': "#00A890",
                        'data3': "#0d89df"
                    },
                    names: {
                        // name of each serie
                        'data1': 'Cluster',
                        'data2': 'Acitivity group',
                        'data3': 'Acitivity'
                    }
                },
                axis: {
                    x: {
                        type: 'category',
                        // name of each category
                        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
                    },
                    rotated: true,
                },
                bar: {
                    width: 16
                },
                legend: {
                    show: true, //hide legend
                },
                padding: {
                    bottom: 0,
                    top: 0
                },
            });
        });
        $(document).ready(function(){
            var chart = c3.generate({
                bindto: '#chart-bar-stacked', // id of chart wrapper
                data: {
                    columns: [
                        // each columns data
                        ['data1', 11, 8, 15, 18, 19, 17],
                        ['data2', 7, 7, 5, 7, 9, 12],
                        ['data3', 9, 5, 10, 18, 15, 12]
                    ],
                    type: 'bar', // default type of chart
                    groups: [
                        [ 'data1', 'data2', 'data3']
                    ],
                    colors: {
                        'data1': "#e3e3e3",
                        'data2': "#00A890",
                        'data3': "#0d89df"
                    },
                    names: {
                        // name of each serie
                        'data1': 'Cluster',
                        'data2': 'Acitivity group',
                        'data3': 'Acitivity'
                    }
                },
                axis: {
                    x: {
                        type: 'category',
                        // name of each category
                        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
                    },
                },
                bar: {
                    width: 30,
                },
                legend: {
                    show: true, //hide legend
                },
                padding: {
                    bottom: 0,
                    top: 0
                },
            });
        });
        $(document).ready(function(){
            var chart = c3.generate({
                bindto: '#chart-pie', // id of chart wrapper
                data: {
                    columns: [
                        // each columns data
                        ['data1', 63],
                        ['data2', 37],
                        ['data3', 63],
                        ['data4', 37],
                        ['data5', 63],
                        ['data6', 37],
                        ['data7', 63],
                        ['data8', 37],
                        ['data9', 63],
                        ['data10', 37],
                        ['data11', 63],
                        ['data12', 37],
                        ['data13', 63],
                        ['data14', 37],
                        ['data15', 63],
                        ['data16', 37],
                        ['data17', 63],
                        ['data18', 37],
                        ['data19', 63],
                        ['data20', 37],
                    ],
                    type: 'pie', // default type of chart
                    
                    colors: {
                        'data1': "#e3e3e3",
                        'data2': "#00A890",
                        'data3': "#0d89df",
                        'data4': "#193f77",
                        'data5': "#f5b2d0",
                        'data6': "#e33d80",
                        'data7': "#a06697",
                        'data8': "#7e545c",
                        'data9': "#418f96",
                        'data10': "#88d7e7",
                        'data11': "#e3e3e3",
                        'data12': "#00A890",
                        'data13': "#0d89df",
                        'data14': "#193f77",
                        'data15': "#f5b2d0",
                        'data16': "#e33d80",
                        'data17': "#a06697",
                        'data18': "#7e545c",
                        'data19': "#418f96",
                        'data20': "#88d7e7",
                    },
                    names: {
                        // name of each serie
                        'data1': 'Activity1',
                        'data2': 'Activity2',
                        'data3': 'Activity3',
                        'data4': 'Activity4',
                        'data5': 'Activity5',
                        'data6': 'Activity6',
                        'data7': 'Activity7',
                        'data8': 'Activity8',
                        'data9': 'Activity9',
                        'data10': 'Activity10',
                        'data11': 'Activity11',
                        'data12': 'Activity12',
                        'data13': 'Activity13',
                        'data14': 'Activity14',
                        'data15': 'Activity15',
                        'data16': 'Activity16',
                        'data17': 'Activity17',
                        'data18': 'Activity18',
                        'data19': 'Activity19',
                        'data20': 'Activity20',
                    }
                },
                axis: {
                },
                legend: {
                    show: true, //hide legend
                },
                padding: {
                    bottom: 0,
                    top: 0
                },
            });
        });
        $(document).ready(function(){
            var chart = c3.generate({
                bindto: '#chart-donut', // id of chart wrapper
                data: {
                    columns: [
                        // each columns data
                        ['data1', 63],
                        ['data2', 37],
                        ['data3', 63],
                        ['data4', 37],
                        ['data5', 63],
                        ['data6', 37],
                        ['data7', 63],
                    ],
                    type: 'donut', // default type of chart
                    
                    colors: {
                        'data1': "#e3e3e3",
                        'data2': "#00A890",
                        'data3': "#0d89df",
                        'data4': "#193f77",
                        'data5': "#f5b2d0",
                        'data6': "#e33d80",
                        'data7': "#a06697",
                    },
                    names: {
                        // name of each serie
                        'data1': 'Verification & Listing',
                        'data2': 'Household awareness creation',
                        'data3': 'Identification of housetype',
                        'data4': 'Finalization of house design',
                        'data5': 'Cost estimation',
                        'data6': 'Verified data',
                        'data7': 'Handover house',
                    }
                },
                donut: {
                    title: "cluster"
                },
                axis: {
                },
                legend: {
                    show: true, //hide legend
                },
                padding: {
                    bottom: 0,
                    top: 0
                },
            });
        });
        $(document).ready(function(){
            var chart = c3.generate({
                bindto: '#chart-scatter', // id of chart wrapper
                data: {
                    columns: [
                        // each columns data
                        ['data1', 11, 8, 15, 18, 19, 17],
                        ['data2', 7, 7, 5, 7, 9, 12]
                    ],
                    type: 'scatter', // default type of chart
                    colors: {
                        'data1': "#00A890",
                        'data2': "#E69A34"
                    },
                    names: {
                        // name of each serie
                        'data1': 'Maximum',
                        'data2': 'Minimum'
                    }
                },
                axis: {
                    x: {
                        type: 'category',
                        // name of each category
                        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
                    },
                },
                legend: {
                    show: true, //hide legend
                },
                padding: {
                    bottom: 0,
                    top: 0
                },
            });
        });
        $(document).ready(function(){
            var chart = c3.generate({
                bindto: '#bar-chart', // id of chart wrapper
                data: {
                    columns: [
                        // each columns data
                        ['data1', 30, 20, 50, 40, 60, 50],
                        ['data2', 200, 130, 90, 240, 130, 220],
                        ['data3', 300, 200, 160, 400, 250, 250],
                        ['data4', 200, 130, 90, 240, 130, 220]
                    ],
                    type: 'bar', // default type of chart
                    types: {
                        'data2': "line",
                        'data3': "spline",
                    },
                    groups: [
                        [ 'data1', 'data4']
                    ],
                    colors: {
                        'data1': "#00A890",
                        'data2': "#E69A34",
                        'data3': "#e3e3e3",
                        'data4': "#0d89df"
                    },
                    names: {
                        // name of each serie
                        'data1': 'Output',
                        'data2': 'Cluster',
                        'data3': 'Activity group',
                        'data4': 'Activity'
                    }
                },
                axis: {
                    x: {
                        type: 'category',
                        // name of each category
                        categories: ['2013', '2014', '2015', '2016', '2019', '2018']
                    },
                },
                bar: {
                    width: 30,
                },
                legend: {
                    show: true, //hide legend
                },
                padding: {
                    bottom: 0,
                    top: 0
                },
            });
        });
        $(document).ready(function(){
            var chart = c3.generate({
                bindto: '#chart-single', // id of chart wrapper
                data: {
                    columns: [
                        // each columns data
                        ['data1', 100, 200, 300, 250, 350, 150,500,1000,400, 800],
                    ],
                    type: 'bar', // default type of chart
                    
                    colors: {
                        'data1': "#00A890",
                    },
                    names: {
                        // name of each serie
                        'data1': 'marginlized',
                    }
                },
                axis: {
                    x: {
                        type: 'category',
                        // name of each category
                        categories: ['Household awareness creation', 'verification and listing', 'Household awareness creation', 'verification and listing' , 'Household awareness creation', 'verification and listing' , 'Household awareness creation', 'verification and listing' , 'Household awareness creation', 'verification and listing' ],
                        
                    },
                },
                bar: {
                    width: 16
                },
                legend: {
                    show: true, //hide legend
                    position: 'inset',
                    inset: {
                            anchor: 'top-right',
                            x: 50,
                            y: -30,
                            step: 1
                        }
                },
                padding: {
                    bottom: 0,
                    top: 30
                },
            });
        });
    }, 500);
});