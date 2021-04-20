$(document).ready(function() {

  // Read data file and create a chart
  $.get(dataurl, function(csvString) {

      var TITLE = 'PANDA benchmarks';
    
    
      // `false` for vertical column chart, `true` for horizontal bar chart
      var HORIZONTAL = false;
    
      // `false` for individual bars, `true` for stacked bars
      var STACKED = false;  
      
      // Which column defines 'bucket' names?
      var LABELS = 'method'; 
    
    
      colors='#0f6efd'
    
    
      // For each column representing a data series, define its name and color
        var SERIES = [  
          {
            column: 'ko',
            name: 'AUROC',
            color: colors
          }
        ];
        var SERIES2 = [  
          {
            column: 'cc',
            name: 'AUROC',
            color: colors
          }
        ];
        var SERIES3 = [  
          {
            column: 'sr',
            name: 'AUROC',
            color: colors
          }
        ];

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

    
    
      // x-axis label and label in tooltip
      var X_AXIS = 'Method';
    
      // y-axis label, label in tooltip
      var Y_AXIS = 'AUROC';
    
      // `true` to show the grid, `false` to hide
      var SHOW_GRID = true; 
    
      // `true` to show the legend, `false` to hide
      var SHOW_LEGEND = true; 
    
      // Read data file and create a chart
     
    
        //var rows = Papa.parse(csvString, {header: true}).data;
        var rows=data2
        var rowsdrag=data2drag
    
        var datasets1 = SERIES.map(function(el) {
          return {
            label: el.name,
            labelDirty: el.column,
            backgroundColor: el.color,
            data: []
          }
        });
        var datasets2 = SERIES2.map(function(el) {
          return {
            label: el.name,
            labelDirty: el.column,
            backgroundColor: el.color,
            data: []
          }
        });
        var datasets3 = SERIES3.map(function(el) {
          return {
            label: el.name,
            labelDirty: el.column,
            backgroundColor: el.color,
            data: []
          }
        });

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

    
    
        rows.map(function(row) {
          datasets1.map(function(d) {
            d.data.push(row.fields[d.labelDirty])
          })
        });

        rows.map(function(row) {
          datasets2.map(function(d) {
            d.data.push(row.fields[d.labelDirty])
          })
        });

        rows.map(function(row) {
          datasets3.map(function(d) {
            d.data.push(row.fields[d.labelDirty])
          })
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



      var barChartData = {
          labels: rows.map(function(el) { return el.fields[LABELS] }),
          datasets: [
            {
              label:'KO',
              data:datasets1[0].data,
              backgroundColor: '#c8224a',
            },
            {
              label:'CC',
              data:datasets2[0].data,
              backgroundColor: '#3466e6',
            },
            {
              label:'SR',
              data:datasets3[0].data,
              backgroundColor: '#23b14d',
            }
          ]
        };



        var barChartDatadragon = {
          labels: rowsdrag.map(function(el) { return el.fields[LABELS] }),
          datasets: [
            {
              label:'DRAGON',
              data:datasets4[0].data,
              backgroundColor: '#c8224a',
            },
            {
              label:'GGM',
              data:datasets5[0].data,
              backgroundColor: '#3466e6',
            }
          ]
        };
    
        //console.log(datasets)
    
        var canvasbar = document.getElementById('cellbar');
        var ctx    = canvasbar.getContext('2d');
        var canvasbardragon = document.getElementById('dragonbar');
        var ctxdragon    = canvasbardragon.getContext('2d');
    
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


        var X_AXIS = 'Sample size';
        var TITLE = 'DRAGON benchmarks';

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
    
  });


});