$(document).ready(function() {

  var TITLE = 'Number of TFs';

  // `false` for vertical column chart, `true` for horizontal bar chart
  var HORIZONTAL = false;

	// `false` for individual bars, `true` for stacked bars
  var STACKED = false;  
  
  // Which column defines 'bucket' names?
  var LABELS = 'dispname';  

  colors='#ffc107'

  // For each column representing a data series, define its name and color
    var SERIES = [  
      {
        column: 'ntfs',
        name: 'Number of TFs',
        color: colors
      }
    ];

  // x-axis label and label in tooltip
  var X_AXIS = 'Cancer types';

  // y-axis label, label in tooltip
  var Y_AXIS = 'Number of TFs';

  // `true` to show the grid, `false` to hide
  var SHOW_GRID = true; 

  // `true` to show the legend, `false` to hide
  var SHOW_LEGEND = false; 

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

    var canvasbar1 = document.getElementById('cancerbubble');
    var ctx    = canvasbar1.getContext('2d');

    var barchart1 = new Chart(ctx, {
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

    // GENES
    var TITLE = 'Number of genes';

    // `false` for vertical column chart, `true` for horizontal bar chart
    var HORIZONTAL = false;
  
    // `false` for individual bars, `true` for stacked bars
    var STACKED = false;  
    
    // Which column defines 'bucket' names?
    var LABELS = 'dispname';  
  
    colors='#28a744'
  
    // For each column representing a data series, define its name and color
      var SERIES = [  
        {
          column: 'ngenes',
          name: 'Number of genes',
          color: colors
        }
      ];
  
    // x-axis label and label in tooltip
    var X_AXIS = 'Cancer types';
  
    // y-axis label, label in tooltip
    var Y_AXIS = 'Number of Genes';
  
    // `true` to show the grid, `false` to hide
    var SHOW_GRID = true; 
  
    // `true` to show the legend, `false` to hide
    var SHOW_LEGEND = false; 
  
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
  
      var canvasbar2 = document.getElementById('cancerbubble2');
      var ctx    = canvasbar2.getContext('2d');
  
      var barchart2 = new Chart(ctx, {
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
  
      


    // Patients
    var TITLE = 'Number of patients';

    // `false` for vertical column chart, `true` for horizontal bar chart
    var HORIZONTAL = false;
  
    // `false` for individual bars, `true` for stacked bars
    var STACKED = false;  
    
    // Which column defines 'bucket' names?
    var LABELS = 'dispname';  
  
    colors='#db3646'
  
    // For each column representing a data series, define its name and color
      var SERIES = [  
        {
          column: 'nsamples',
          name: 'Number of samples',
          color: colors
        }
      ];
  
    // x-axis label and label in tooltip
    var X_AXIS = 'Cancer types';
  
    // y-axis label, label in tooltip
    var Y_AXIS = 'Number of patients';
  
    // `true` to show the grid, `false` to hide
    var SHOW_GRID = true; 
  
    // `true` to show the legend, `false` to hide
    var SHOW_LEGEND = false; 
  
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
  
      var canvasbar3 = document.getElementById('cancerbubble3');
      var ctx    = canvasbar3.getContext('2d');
  
      var barchart3 = new Chart(ctx, {
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
  

      var table = $('#tissuestable').DataTable({
        "serverSide": false,
        "processing": true,
               "dom": "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-5'f>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
       });

       canvasbar1.onclick = function(evt) {
        var activePoints = barchart1.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var label = activePoints[0]._view['label'];
          if (label=='GBM TCGA 1' | label=='GBM TCGA 2'){
            label='GBM'
          }
          table.search(label).draw();
        }
      };

      canvasbar2.onclick = function(evt) {
        var activePoints = barchart2.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var label = activePoints[0]._view['label'];
          if (label=='GBM TCGA 1' | label=='GBM TCGA 2'){
            label='GBM'
          }
          table.search(label).draw();
        }
      };

      canvasbar3.onclick = function(evt) {
        var activePoints = barchart3.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var label = activePoints[0]._view['label'];
          if (label=='GBM TCGA 1' | label=='GBM TCGA 2'){
            label='GBM'
          }
          table.search(label).draw();
        }
      };

});
