$(document).ready(function() {

    
    
  // `false` for vertical column chart, `true` for horizontal bar chart
  var HORIZONTAL = false;

  // `false` for individual bars, `true` for stacked bars
  var STACKED = false;  

    
  var SHOW_GRID = true; // `true` to show the grid, `false` to hide
  colors='#0f6efd'
  
      // x-axis label and label in tooltip
    
      // `true` to show the grid, `false` to hide
      var SHOW_GRID = true; 
    
      // `true` to show the legend, `false` to hide
      var SHOW_LEGEND = true; 

        var rowsdrag=data2

        var LABELS = 'sig_id'; 

        var SERIES4 = [  
          {
            column: 'diffexp',
            name: 'AUROC',
            color: colors
          }
        ];
        var SERIES5 = [  
          {
            column: 'difftar',
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
              label:'TF expression',
              data:datasets4[0].data,
              backgroundColor: '#c8224a',
            },
            {
              label:'TF targeting',
              data:datasets5[0].data,
              backgroundColor: '#3466e6',
            }
          ]
        };
    
        var canvasbardragon = document.getElementById('cellbartf');
        var ctxdragon    = canvasbardragon.getContext('2d');

        var X_AXIS = 'L1000 signature ID';
        var Y_AXIS = 'Number of TFs';
        var TITLE = 'Differentially expressed and targeted TFs for ' + drugname;

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
          var idx = activePoints[0]['_index'];
          if (activePoints[0]) {
            location.href = '/networks/drugtarg/' + rowsdrag[idx].fields['cleannames']
          }
        };











            
    
  // `false` for vertical column chart, `true` for horizontal bar chart
  var HORIZONTAL = false;

  // `false` for individual bars, `true` for stacked bars
  var STACKED = false;  

    
  var SHOW_GRID = true; // `true` to show the grid, `false` to hide
  colors='#0f6efd'
  
        // x-axis label and label in tooltip
    
      // `true` to show the grid, `false` to hide
      var SHOW_GRID = true; 
    
      // `true` to show the legend, `false` to hide
      var SHOW_LEGEND = true; 

        var rowsdrag=data2

        var LABELS = 'sig_id'; 

        var SERIES4 = [  
          {
            column: 'diffexpgenes',
            name: 'AUROC',
            color: colors
          }
        ];
        var SERIES5 = [  
          {
            column: 'difftargenes',
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
              label:'Gene expression',
              data:datasets4[0].data,
              backgroundColor: '#c8224a',
            },
            {
              label:'Gene targeting',
              data:datasets5[0].data,
              backgroundColor: '#3466e6',
            }
          ]
        };
    
        var canvasbardragon = document.getElementById('cellbargenes');
        var ctxdragon    = canvasbardragon.getContext('2d');

        var X_AXIS = 'L1000 signature ID';
        var Y_AXIS = 'Number of genes';
        var TITLE = 'Differentially expressed and targeted genes for ' + drugname;

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
          var idx = activePoints[0]['_index'];
          if (activePoints[0]) {
            location.href = '/networks/drugtarg/' + rowsdrag[idx].fields['cleannames']
          }
        };


});