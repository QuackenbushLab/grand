$(document).ready(function() {


  
        var TITLE = 'TF targeting score';
        var TITLE2 = 'Gene targeting score';
      
      
        // `false` for vertical column chart, `true` for horizontal bar chart
        var HORIZONTAL = false;
      
        // `false` for individual bars, `true` for stacked bars
        var STACKED = false;  
        
        // Which column defines 'bucket' names?
        var LABELS = 'TF'; 
        var LABELS2 = 'index'; 
      
      
        colors='#0f6efd'
        colors2='#28a744'
      
      
        // For each column representing a data series, define its name and color
          var SERIES = [  
            {
              column: 'tar',
              name: 'Targeting score',
              color: colors
            }
          ];
          var SERIES2 = [  
            {
              column: 'tar',
              name: 'Targeting score',
              color: colors2
            }
          ];
      
      
        // x-axis label and label in tooltip
        var X_AXIS = 'Transcription factor';
        var X_AXIS2 = 'Gene';
      
        // y-axis label, label in tooltip
        var Y_AXIS = 'Standardized targeting (Z-score)';
      
        // `true` to show the grid, `false` to hide
        var SHOW_GRID = true; 
      
        // `true` to show the legend, `false` to hide
        var SHOW_LEGEND = false; 
      
        // Read data file and create a chart
       
      
          //var rows = Papa.parse(csvString, {header: true}).data;
        var rows=tftarscore
        var rows2=genetarscore
      
        var datasets1 = SERIES.map(function(el) {
            return {
              label: el.name,
              labelDirty: el.column,
              backgroundColor: el.color,
              data: []
            }
        });
      
        rows.map(function(row) {
            datasets1.map(function(d) {
              d.data.push(row[d.labelDirty])
            })
        });

        var datasets2 = SERIES2.map(function(el) {
            return {
              label: el.name,
              labelDirty: el.column,
              backgroundColor: el.color,
              data: []
            }
        });
      
        rows2.map(function(row) {
            datasets2.map(function(d) {
              d.data.push(row[d.labelDirty])
            })
        });
  
        var barChartData = {
            labels: rows.map(function(el) { return el[LABELS] }),
            datasets: datasets1
          };

          var barChartDataGene = {
            labels: rows2.map(function(el) { return el[LABELS2] }),
            datasets: datasets2
          };

          //console.log(datasets)
          var canvasbar = document.getElementById('genetardiv');
          var ctx    = canvasbar.getContext('2d');
          var canvasbartf = document.getElementById('tftardiv');
          var ctxtf    = canvasbartf.getContext('2d');

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


          var barcharttf = new Chart(ctxtf, {
            type: HORIZONTAL ? 'horizontalBar' : 'bar',
            data: barChartDataGene,
            
            options: {
              title: {
                display: true,
                text: TITLE2,
                fontSize: 14,
              },
              legend: {
                display: SHOW_LEGEND,
              },
              scales: {
                xAxes: [{
                  stacked: STACKED,
                  scaleLabel: {
                    display: X_AXIS2 !== '',
                    labelString: X_AXIS2
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