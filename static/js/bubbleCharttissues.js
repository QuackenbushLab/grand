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

  var POINT_NAME = 'tissue'; // point names that appear in tooltip
  var POINT_COLOR = 'rgba(0,0,255,0.7)'; // eg `black` or `rgba(10,100,44,0.8)`

  var REG_NAME = 'reg'
  var X_AXIS_C = 'Number of cells'; // x-axis label, label in tooltip
  var Y_AXIS_C = 'Number of genes'; // y-axis label, label in tooltip

  var SHOW_GRID = true; // `true` to show the grid, `false` to hide

  // Read data file and create a chart


      var TITLE = 'Human single-sample tissue network models';
    
    
      // `false` for vertical column chart, `true` for horizontal bar chart
      var HORIZONTAL = false;
    
      // `false` for individual bars, `true` for stacked bars
      var STACKED = false;  
      
      // Which column defines 'bucket' names?
      var LABELS = 'tissuename'; 
    
    
      colors='#0f6efd'
    
    
      // For each column representing a data series, define its name and color
      var SERIES = [  
        {
          column: 'nsamples',
          name: 'Number of patients',
          color: colors
        }
      ];
    
    
        // x-axis label and label in tooltip
        var X_AXIS = 'Tissue type';
      
        // y-axis label, label in tooltip
        var Y_AXIS = 'Number of patients';
    
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
        // Add event listener for opening and closing details
        canvasbar.onclick = function(evt) {
          var activePoints = barchart.getElementsAtEvent(evt);
          if (activePoints[0]) {
            var label = activePoints[0]._view['label'];
            table.search(label).draw();
          }
        };
    
        
    
    




    


  


        var rowsdrag=data2drag

        var LABELS = 'method'; 

        var SERIES4 = [  
          {
            column: 'ko',
            name: 'AUROC',
            color: colors
          }
        ];
        var SERIES5 = [  
          {
            column: 'cc',
            name: 'AUROC',
            color: colors
          }
        ];


    
        var datasets4 = SERIES4.map(function(el) {
          return {
            label: el.name,
            labelDirty: el.column,
            backgroundColor: el.color,
            data: []
          }
        });
        var datasets5 = SERIES5.map(function(el) {
          return {
            label: el.name,
            labelDirty: el.column,
            backgroundColor: el.color,
            data: []
          }
        });

    
    

        rowsdrag.map(function(row) {
          datasets4.map(function(d) {
            d.data.push(row.fields[d.labelDirty])
          })
        });

        rowsdrag.map(function(row) {
          datasets5.map(function(d) {
            d.data.push(row.fields[d.labelDirty])
          })
        });


        var barChartDatadragon = {
          labels: rowsdrag.map(function(el) { return el.fields[LABELS] }),
          datasets: [
            {
              label:'Genes',
              data:datasets4[0].data,
              backgroundColor: '#c8224a',
            },
            {
              label:'Regulators',
              data:datasets5[0].data,
              backgroundColor: '#3466e6',
            }
          ]
        };
    
        var canvasbardragon = document.getElementById('cancerbubble');
        var ctxdragon    = canvasbardragon.getContext('2d');

        var X_AXIS = 'Network type';
        var Y_AXIS = 'Number of network nodes';
        var TITLE = 'Network size per regulation type';

        var barchartdragon = new Chart(ctxdragon, {
          type: HORIZONTAL ? 'horizontalBar' : 'bar',
          data: barChartDatadragon,
          
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

        canvasbardragon.onclick = function(evt) {
          var activePoints = barchartdragon.getElementsAtEvent(evt);
          if (activePoints[0]) {
            var label = activePoints[0]._view['label'];
            if(label=='miRNA network'){
              label='miRNA'
            }else{
              label='TF'
            }
            table.search(label).draw();
          }
        };




});