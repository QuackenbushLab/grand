$(document).ready(function() {
  var rows=data2
  var TITLE_C = 'Small molecule gene regulatory networks';

  var POINT_X = 'avggenetar'; // column name for x values in data.csv
  var POINT_X_PREFIX = ''; // prefix for x values, eg '$'
  var POINT_X_POSTFIX = ''; // postfix for x values, eg '%'

  var POINT_Y = 'avgtftar'; // column name for y values in data.csv
  var POINT_Y_PREFIX = ''; // prefix for x values, eg 'USD '
  var POINT_Y_POSTFIX = ''; // postfix for x values, eg ' kg'

  var POINT_R = 'nsamples'; // column name for radius in data.csv
  var POINT_R_DESCRIPTION = 'Samples'; // description of radius value
  var POINT_R_PREFIX = ''; // prefix for radius values, eg 'USD '
  var POINT_R_POSTFIX = ' '; // postfix for radius values, eg ' kg'
  var R_DENOMINATOR = 20;  // use this to scale the dot sizes, or set to 1
                            // if your dataset contains precise radius values

  var POINT_NAME = 'drug'; // point names that appear in tooltip
  var POINT_COLOR = 'rgba(71,91,253,0.6)'; // eg `black` or `rgba(10,100,44,0.8)`

  var REG_NAME = 'nsamples'
  var X_AXIS_C = 'Average number of differentially targeted genes'; // x-axis label, label in tooltip
  var Y_AXIS_C = 'Average number of differentially targeted TFs'; // y-axis label, label in tooltip

  var SHOW_GRID = true; // `true` to show the grid, `false` to hide

  // Read data file and create a chart

      var TITLE = 'Cancer cell lines';
    
    
      // `false` for vertical column chart, `true` for horizontal bar chart
      var HORIZONTAL = false;
    
      // `false` for individual bars, `true` for stacked bars
      var STACKED = false;  
      
      // Which column defines 'bucket' names?
      var LABELS = 'disease'; 
    
    
    
    
      // For each column representing a data series, define its name and color
    
    
      // x-axis label and label in tooltip
      var X_AXIS = 'Cancer type';
    
      // y-axis label, label in tooltip
      var Y_AXIS = 'Number of cells';
    
      // `true` to show the grid, `false` to hide
      var SHOW_GRID = true; 
    
      // `true` to show the legend, `false` to hide
      var SHOW_LEGEND = false; 
    
      // Read data file and create a chart
    
        
    
    

    console.log(rows)

    var data = rows.map(function(row) {
      return {
        x: row.fields[POINT_X],
        y: row.fields[POINT_Y],
        r: Math.log(row.fields[POINT_R]),
        rr: row.fields[POINT_R],
        name: row.fields[POINT_NAME],
        reg: row[REG_NAME]
      }
    })

    console.log(data)

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
            type: 'logarithmic',
            scaleLabel: {
              display: true,
              labelString: X_AXIS_C
            },
            gridLines: {
              display: SHOW_GRID,
            },
            ticks: {
              min: 10, //minimum tick
              max: 3000, //maximum tick
              autoSkip: true,
              callback: function (value, index, values) {
                  if( value==10 || value==100 || value==1000 || value==10000 || value==100000  || value==3000){
                      return value ;
                  }
              },                  

            }
          }],
          yAxes: [{
            type: 'logarithmic',
            scaleLabel: {
              display: true,
              labelString: Y_AXIS_C
            },
            gridLines: {
              display: SHOW_GRID,
            },
            ticks: {
              min: 0, //minimum tick
              max: 200, //maximum tick
              callback: function (value, index, values) {
                if( value==0 || value==10 || value==100 || value==200 || value==100000  || value==1000000){
                    return value ;
                }
            },    
            }
          }],
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
              var rr = all.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].rr;
              return [
                X_AXIS_C + ': ' + POINT_X_PREFIX + tooltipItem.xLabel.toLocaleString() + POINT_X_POSTFIX,
                Y_AXIS_C + ': ' + POINT_Y_PREFIX + tooltipItem.yLabel.toLocaleString() + POINT_Y_POSTFIX,
                POINT_R_DESCRIPTION + ': ' + POINT_R_PREFIX + rr.toLocaleString() 
              ]
            }
          }
        }
      }
    });

    var table = $('#drugstable').DataTable({
      "ajax": "https://grand.networkmedicine.org/api/v1/drugapi/?format=datatables",
 
      "serverSide": true,
      "processing": true,
 
       "columns": [
           {"data": "number"},
           {"data": "druglink"},
           {"data": "nsamples"},
           {"data": "avgtftar"},
           {"data": "avggenetar"},
           {"data": "moa"},
           {"data": "indication"},
       ],
 
       "dom": "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-5'f>>" +
              "<'row'<'col-sm-12'tr>>" +
              "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
     });

    canvas.onclick = function(evt) {
      var activePoints = myNewChart.getElementsAtEvent(evt);
      if (activePoints[0]) {
        var chartData = activePoints[0]['_chart'].config.data;
        var idx = activePoints[0]['_index'];
  
        var label = chartData.datasets[0].data[idx].name;
        console.log(label)
        table.search(label).draw();
      }
    };



});