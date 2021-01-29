$(document).ready(function() {

  var TITLE = 'Cancer gene regulatory networks';

  var POINT_X = 'samples'; // column name for x values in data.csv
  var POINT_X_PREFIX = ''; // prefix for x values, eg '$'
  var POINT_X_POSTFIX = ''; // postfix for x values, eg '%'

  var POINT_Y = 'genes'; // column name for y values in data.csv
  var POINT_Y_PREFIX = ''; // prefix for x values, eg 'USD '
  var POINT_Y_POSTFIX = ''; // postfix for x values, eg ' kg'

  var POINT_R = 'tfs'; // column name for radius in data.csv
  var POINT_R_DESCRIPTION = 'Regulators'; // description of radius value
  var POINT_R_PREFIX = ''; // prefix for radius values, eg 'USD '
  var POINT_R_POSTFIX = ' TFs'; // postfix for radius values, eg ' kg'
  var R_DENOMINATOR = 80;  // use this to scale the dot sizes, or set to 1
                            // if your dataset contains precise radius values

  var POINT_NAME = 'cancer'; // point names that appear in tooltip
  var POINT_COLOR = 'rgba(0,0,255,0.7)'; // eg `black` or `rgba(10,100,44,0.8)`

  var X_AXIS = 'Number of patients'; // x-axis label, label in tooltip
  var Y_AXIS = 'Number of genes'; // y-axis label, label in tooltip

  var SHOW_GRID = true; // `true` to show the grid, `false` to hide

  // Read data file and create a chart
  $.get(dataurl, function(csvString) {

    var rows = Papa.parse(csvString, {header: true}).data;

    var data = rows.map(function(row) {
      return {
        x: row[POINT_X],
        y: row[POINT_Y],
        r: row[POINT_R] / R_DENOMINATOR,
        name: row[POINT_NAME]
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
          text: TITLE,
          fontSize: 14,
        },
        legend: {
          display: false,
        },
        scales: {
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: X_AXIS
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
              labelString: Y_AXIS
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
              return [
                X_AXIS + ': ' + POINT_X_PREFIX + tooltipItem.xLabel.toLocaleString() + POINT_X_POSTFIX,
                Y_AXIS + ': ' + POINT_Y_PREFIX + tooltipItem.yLabel.toLocaleString() + POINT_Y_POSTFIX,
                POINT_R_DESCRIPTION + ': ' + POINT_R_PREFIX + r.toLocaleString() + POINT_R_POSTFIX
              ]
            }
          }
        }
      }
    });

    var table = $('#tissuestable').DataTable({
      "dom": "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-5'f>>" +
             "<'row'<'col-sm-12'tr>>" +
             "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
    });

    canvas.onclick = function(evt) {
      var activePoints = myNewChart.getElementsAtEvent(evt);
      if (activePoints[0]) {
        var chartData = activePoints[0]['_chart'].config.data;
        var idx = activePoints[0]['_index'];
  
        var label = chartData.datasets[0].data[idx].name  //chartData.labels[idx]; 
        var value = chartData.datasets[0].data[idx];
        console.log(label);
        table.search(label).draw();
      }
    };

  });


});