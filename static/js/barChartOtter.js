$(document).ready(function() {

  // Read data file and create a chart
  $.get(dataurl, function(csvString) {

      var TITLE = 'OTTER benchmarks';
    
    
      // `false` for vertical column chart, `true` for horizontal bar chart
      var HORIZONTAL = false;
    
      // `false` for individual bars, `true` for stacked bars
      var STACKED = false;  
      
      // Which column defines 'bucket' names?
      var LABELS = 'method'; 
    
    
      colors='#0f6efd'
    
    
      // For each column representing a data series, define its name and color
      if (slug=='Breast_cancer'){
        var SERIES = [  
          {
            column: 'aurocbr',
            name: 'AUROC',
            color: colors
          }
        ];
      }else if (slug=='Cervix_cancer'){
        var SERIES = [  
          {
            column: 'auroccer',
            name: 'AUROC',
            color: colors
          }
        ];
      }else if (slug='Liver_cancer'){
        var SERIES = [  
          {
            column: 'aurocliv',
            name: 'AUROC',
            color: colors
          }
        ];
      }
    
    
      // x-axis label and label in tooltip
      var X_AXIS = 'Method';
    
      // y-axis label, label in tooltip
      var Y_AXIS = 'AUROC';
    
      // `true` to show the grid, `false` to hide
      var SHOW_GRID = true; 
    
      // `true` to show the legend, `false` to hide
      var SHOW_LEGEND = false; 
    
      // Read data file and create a chart
     
    
        //var rows = Papa.parse(csvString, {header: true}).data;
        var rows=data2
        console.log(rows)
    
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




    
    
        // `false` for vertical column chart, `true` for horizontal bar chart
        var HORIZONTAL = false;
      
        // `false` for individual bars, `true` for stacked bars
        var STACKED = false;  
        
        // Which column defines 'bucket' names?
        var LABELS = 'method'; 
      
      
        colors='#0f6efd'
      
      
        // For each column representing a data series, define its name and color
      // For each column representing a data series, define its name and color
      if (slug=='Breast_cancer'){
        var SERIES = [  
          {
            column: 'auprbr',
            name: 'AUPR',
            color: colors
          }
        ];
      }else if (slug=='Cervix_cancer'){
        var SERIES = [  
          {
            column: 'auprcer',
            name: 'AUPR',
            color: colors
          }
        ];
      }else if (slug='Liver_cancer'){
        var SERIES = [  
          {
            column: 'auprliv',
            name: 'AUPR',
            color: colors
          }
        ];
      }
      
      
        // x-axis label and label in tooltip
        var X_AXIS = 'Method';
      
        // y-axis label, label in tooltip
        var Y_AXIS = 'AUPR';
      
        // `true` to show the grid, `false` to hide
        var SHOW_GRID = true; 
      
        // `true` to show the legend, `false` to hide
        var SHOW_LEGEND = false; 
      
        // Read data file and create a chart
       
      
          //var rows = Papa.parse(csvString, {header: true}).data;
          var rows=data2
          console.log(rows)
      
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
      
          var canvasbar = document.getElementById('cellbarpr');
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
    
  });


});