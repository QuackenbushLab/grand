$(document).ready(function() {

  var TITLE = 'Enriched GO terms in differentially targeted TFs';

  // `false` for vertical column chart, `true` for horizontal bar chart
  var HORIZONTAL = false;

	// `false` for individual bars, `true` for stacked bars
  var STACKED = false;  
  
  // Which column defines 'bucket' names?
  var LABELS = 'term';  

  colors='#ffc107'

  // For each column representing a data series, define its name and color
    var SERIES = [  
      {
        column: 'logpval',
        name: '-log10(pval)',
        color: colors,
        labels2: 'go'
      }
    ];

  // x-axis label and label in tooltip
  var X_AXIS = 'GO terms';

  // y-axis label, label in tooltip
  var Y_AXIS = '-log10(p-value)';

  // `true` to show the grid, `false` to hide
  var SHOW_GRID = true; 

  // `true` to show the legend, `false` to hide
  var SHOW_LEGEND = false; 

  //var rows = Papa.parse(csvString, {header: true}).data;
  var rows=data5tfs

  var datasets = SERIES.map(function(el) {
      return {
        label: el.name,
        labelDirty: el.column,
        backgroundColor: el.color,
        data: [],
        labels2: [],
      }
    });


  rows.map(function(row) {
      datasets.map(function(d) {
        d.data.push(row.fields[d.labelDirty])
        d.labels2.push(row.fields['go'])
      })
    });

	var barChartData = {
      labels: rows.map(function(el) { return el.fields[LABELS] }),    
			datasets: datasets
    };

    var canvasbar1 = document.getElementById('cancerbubble2');
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
              var reg = all.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].labels2;
              return [
              all.datasets[tooltipItem.datasetIndex].labels2[tooltipItem.index],
              all.datasets[tooltipItem.datasetIndex].label + ': ' + tooltipItem.yLabel.toLocaleString() ,
              ]
            }
          }
        }
      }
    });

    // GENES

    var TITLE = 'Enriched GO terms in differentially targeted genes';

    // `false` for vertical column chart, `true` for horizontal bar chart
    var HORIZONTAL = false;
  
    // `false` for individual bars, `true` for stacked bars
    var STACKED = false;  
    
    // Which column defines 'bucket' names?
    var LABELS = 'term';  
  
    colors='#28a744'
  
    // For each column representing a data series, define its name and color
      var SERIES = [  
        {
          column: 'logpval',
          name: '-log10(pval)',
          color: colors,
          labels2: 'go'
        }
      ];
  
    // x-axis label and label in tooltip
    var X_AXIS = 'GO terms';
  
    // y-axis label, label in tooltip
    var Y_AXIS = '-log10(p-value)';
  
    // `true` to show the grid, `false` to hide
    var SHOW_GRID = true; 
  
    // `true` to show the legend, `false` to hide
    var SHOW_LEGEND = false; 
  
    //var rows = Papa.parse(csvString, {header: true}).data;
    var rows=data5genes
  
    var datasets = SERIES.map(function(el) {
        return {
          label: el.name,
          labelDirty: el.column,
          backgroundColor: el.color,
          data: [],
          labels2: [],
        }
      });
  
  
    rows.map(function(row) {
        datasets.map(function(d) {
          d.data.push(row.fields[d.labelDirty]),
          d.labels2.push(row.fields['go'])          
        })
      });
  
    var barChartData = {
        labels: rows.map(function(el) { return el.fields[LABELS] }),
        datasets: datasets
      };
  
      var canvasbar2 = document.getElementById('cancerbubble3');
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
                return [
                  all.datasets[tooltipItem.datasetIndex].labels2[tooltipItem.index],
                  all.datasets[tooltipItem.datasetIndex].label + ': ' + tooltipItem.yLabel.toLocaleString() ,
                  ]
              }
            }
          }
        }
      });
  
      



});
