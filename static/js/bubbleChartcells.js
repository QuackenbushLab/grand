$(document).ready(function() {

  var TITLE_C = 'Cell line gene regulatory networks';

  var POINT_X = 'samples'; // column name for x values in data.csv
  var POINT_X_PREFIX = ''; // prefix for x values, eg '$'
  var POINT_X_POSTFIX = ''; // postfix for x values, eg '%'

  var POINT_Y = 'genes'; // column name for y values in data.csv
  var POINT_Y_PREFIX = ''; // prefix for x values, eg 'USD '
  var POINT_Y_POSTFIX = ''; // postfix for x values, eg ' kg'

  var POINT_R = 'tfs'; // column name for radius in data.csv
  var POINT_R_DESCRIPTION = 'Regulators'; // description of radius value
  var POINT_R_PREFIX = ''; // prefix for radius values, eg 'USD '
  var POINT_R_POSTFIX = ' '; // postfix for radius values, eg ' kg'
  var R_DENOMINATOR = 60;  // use this to scale the dot sizes, or set to 1
                            // if your dataset contains precise radius values

  var POINT_NAME = 'cancer'; // point names that appear in tooltip
  var POINT_COLOR = 'rgba(0,0,255,0.7)'; // eg `black` or `rgba(10,100,44,0.8)`

  var REG_NAME = 'reg'
  var X_AXIS_C = 'Number of cells'; // x-axis label, label in tooltip
  var Y_AXIS_C = 'Number of genes'; // y-axis label, label in tooltip

  var SHOW_GRID = true; // `true` to show the grid, `false` to hide

  // Read data file and create a chart
  $.get(dataurl, function(csvString) {

      var TITLE = 'Cancer cell lines';
    
    
      // `false` for vertical column chart, `true` for horizontal bar chart
      var HORIZONTAL = false;
    
      // `false` for individual bars, `true` for stacked bars
      var STACKED = false;  
      
      // Which column defines 'bucket' names?
      var LABELS = 'disease'; 
    
    
      colors='#0f6efd'
    
    
      // For each column representing a data series, define its name and color
        var SERIES = [  
          {
            column: 'ncells',
            name: 'Number of cells',
            color: colors
          }
        ];
    
    
      // x-axis label and label in tooltip
      var X_AXIS = 'Cancer type';
    
      // y-axis label, label in tooltip
      var Y_AXIS = 'Number of cells';
    
      // `true` to show the grid, `false` to hide
      var SHOW_GRID = true; 
    
      // `true` to show the legend, `false` to hide
      var SHOW_LEGEND = false; 
    
      // Read data file and create a chart
     
    
        //var rows = Papa.parse(csvString, {header: true}).data;
        var rows=data2
    
        var datasets = SERIES.map(function(el) {
          return {
            label: el.name,
            labelDirty: el.column,
            backgroundColor: el.color,
            data: []
          }
        });
    
    
        rows.map(function(row) {
          datasets.map(function(d) {
            d.data.push(row.fields[d.labelDirty])
          })
        });
    
      var barChartData = {
          labels: rows.map(function(el) { return el.fields[LABELS] }),
          datasets: datasets
        };
    
        //console.log(datasets)
    
        var canvasbar = document.getElementById('cellbar');
        var ctx    = canvasbar.getContext('2d');
    
        var barchart = new Chart(ctx, {
          type: HORIZONTAL ? 'horizontalBar' : 'bar',
          data: barChartData,
          
          options: {
            title: {
              display: true,
              text: TITLE,
              fontSize: 14,
            },
            legend: {
              display: SHOW_LEGEND,
            },
            scales: {
              xAxes: [{
                stacked: STACKED,
                scaleLabel: {
                  display: X_AXIS !== '',
                  labelString: X_AXIS
                },
                gridLines: {
                  display: SHOW_GRID,
                },
                ticks: {
                  beginAtZero: true,
                  callback: function(value, index, values) {
                    return value.toLocaleString();
                  }
                }
              }],
              yAxes: [{
                stacked: STACKED,
                beginAtZero: true,
                scaleLabel: {
                  display: Y_AXIS !== '',
                  labelString: Y_AXIS
                },
                gridLines: {
                  display: SHOW_GRID,
                },
                ticks: {
                  beginAtZero: true,
                  callback: function(value, index, values) {
                    return value.toLocaleString()
                  }
                }
              }]
            },
            tooltips: {
              displayColors: false,
              callbacks: {
                label: function(tooltipItem, all) {
                  return all.datasets[tooltipItem.datasetIndex].label
                    + ': ' + tooltipItem.yLabel.toLocaleString();
                }
              }
            }
          }
        });
    
        //datatables
        var table = $('#tissuestable').DataTable({
              "dom": "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-5'f>>" +
                     "<'row'<'col-sm-12'tr>>" +
                     "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
            });
        $("#tissuestable").wrap("<div style='overflow:auto; width:100%;position:relative;'></div>"); 
        // Add event listener for opening and closing details
        canvasbar.onclick = function(evt) {
          var activePoints = barchart.getElementsAtEvent(evt);
          if (activePoints[0]) {
            var label = activePoints[0]._view['label'];
            table.search(label).draw();
          }
        };
    
        
    
    




    var rows = Papa.parse(csvString, {header: true}).data;

    var data = rows.map(function(row) {
      return {
        x: row[POINT_X],
        y: row[POINT_Y],
        r: row[POINT_R] / R_DENOMINATOR,
        name: row[POINT_NAME],
        reg: row[REG_NAME]
      }
    })

		var scatterChartData = {
			datasets: [{
				backgroundColor: POINT_COLOR,
        data: data,
			}]
    };

    var canvas = document.getElementById("cancerbubble");
    var ctx = canvas.getContext("2d");

    var myNewChart = new Chart.Bubble(ctx, {
      data: scatterChartData,
      options: {
        title: {
          display: true,
          text: TITLE_C,
          fontSize: 14,
        },
        legend: {
          display: false,
        },
        scales: {
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: X_AXIS_C
            },
            gridLines: {
              display: SHOW_GRID,
            },
            ticks: {
              callback: function(value, index, values) {
                return POINT_X_PREFIX + value.toLocaleString() + POINT_X_POSTFIX;
              }
            }
          }],
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: Y_AXIS_C
            },
            gridLines: {
              display: SHOW_GRID,
            },
            ticks: {
              callback: function(value, index, values) {
                return POINT_Y_PREFIX + value.toLocaleString() + POINT_Y_POSTFIX;
              }
            }
          }]
        },
        tooltips: {
          displayColors: false,
          callbacks: {
            title: function(tooltipItem, all) {
              return [
                all.datasets[tooltipItem[0].datasetIndex].data[tooltipItem[0].index].name,
              ]
            },
            label: function(tooltipItem, all) {
              var r = all.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].r * R_DENOMINATOR;
              var reg = all.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].reg;
              return [
                X_AXIS_C + ': ' + POINT_X_PREFIX + tooltipItem.xLabel.toLocaleString() + POINT_X_POSTFIX,
                Y_AXIS_C + ': ' + POINT_Y_PREFIX + tooltipItem.yLabel.toLocaleString() + POINT_Y_POSTFIX,
                POINT_R_DESCRIPTION + ': ' + POINT_R_PREFIX + r.toLocaleString() + ' ' + reg
              ]
            }
          }
        }
      }
    });


    canvas.onclick = function(evt) {
      var activePoints = myNewChart.getElementsAtEvent(evt);
      if (activePoints[0]) {
        var chartData = activePoints[0]['_chart'].config.data;
        var idx = activePoints[0]['_index'];
  
        var label = chartData.datasets[0].data[idx].name;
        if (label == 'Normal cells'){
          label = 'Normal'
        }else if (label == 'Cancer cells'){
          label = 'LIONESS'
        }
        table.search(label).draw();
      }
    };

  });


});