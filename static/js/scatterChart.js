$(document).ready(function() {

  if (slug == 'Breast'){
    var TITLE = 'Sample quality control';
  }else{
    var TITLE = 'Height and weight at diagnosis';  
  }

  if (slug == 'Colon'){
    var POINT_X = 'height_cm_at_diagnosis'; // column name for x values in data.csv
  }else if (slug == 'Breast'){
    var POINT_X = 'cgc_slide_percent_tumor_nuclei'; 
  }else{
    var POINT_X = 'gdc_cases.exposures.height'; 
  }
  var POINT_X_PREFIX = ''; // prefix for x values, eg '$'
  var POINT_X_POSTFIX = ''; // postfix for x values, eg '%'

  if (slug == 'Colon'){
    var POINT_Y = 'weight_kg_at_diagnosis'; // column name for y values in data.csv
  }else if (slug == 'Breast'){
    var POINT_Y = 'cgc_slide_percent_necrosis';   
  }else{
    var POINT_Y = 'gdc_cases.exposures.weight'; 
  }

  var POINT_Y_PREFIX = ''; // prefix for x values, eg 'USD '
  var POINT_Y_POSTFIX = ''; // postfix for x values, eg ' kg'

  var POINT_NAME = 'district'; // point names that appear in tooltip
  var POINT_COLOR = 'rgba(54, 162, 235,0.7)'; // eg `black` or `rgba(10,100,44,0.8)`
  var POINT_RADIUS = 5; // radius of each data point

  if (slug == 'Breast'){
    var X_AXIS = 'Tumor nuclei in sample (%)'; // x-axis label, label in tooltip
    var Y_AXIS = 'Necrosis in sample (%) '; // y-axis label, label in tooltip
  }else{
    var X_AXIS = 'Height at diagnosis (cm)'; // x-axis label, label in tooltip
    var Y_AXIS = 'Weight at diagnosis (kg)'; // y-axis label, label in tooltip
  }

  var SHOW_GRID = true; // `true` to show the grid, `false` to hide

  // Read data file and create a chart
  $.get(dataurl, function(csvString) {

    var rows = Papa.parse(csvString, {header: true}).data;

    var data = rows.map(function(row) {
      return {
        x: row[POINT_X],
        y: row[POINT_Y],
        name: row[POINT_NAME]
      }
    })

    var scatterChartData = {
			datasets: [{
				label: 'height weight data',
				backgroundColor: POINT_COLOR,
        data: data,
        pointRadius: POINT_RADIUS,
        pointHoverRadius:  POINT_RADIUS + 2,
			}]
    };

    var ctx = document.getElementById('scatterChart').getContext('2d');

    var myScatterChart = new Chart.Scatter(ctx, {
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
              return [
                X_AXIS + ': ' + POINT_X_PREFIX + tooltipItem.xLabel.toLocaleString() + POINT_X_POSTFIX,
                Y_AXIS + ': ' + POINT_Y_PREFIX + tooltipItem.yLabel.toLocaleString() + POINT_Y_POSTFIX
              ]
            }
          }
        }
      }
    });

  });



  
});


$(document).ready(function() {

    var TITLE = 'Days to death and age at diagnosis';
    if (slug == 'Colon'){
      var POINT_X = 'time_to_event'; // column name for x values in data.csv
    }else{
      var POINT_X = 'gdc_cases.diagnoses.days_to_death'; // column name for x values in data.csv
    }
    var POINT_X_PREFIX = ''; // prefix for x values, eg '$'
    var POINT_X_POSTFIX = ''; // postfix for x values, eg '%'
  
    if (slug == 'Colon'){
      var POINT_Y = 'age_at_initial_pathologic_diagnosis'; // column name for y values in data.csv
    }else{
      var POINT_Y = 'cgc_case_age_at_diagnosis'; // column name for y values in data.csv
    }
    var POINT_Y_PREFIX = ''; // prefix for x values, eg 'USD '
    var POINT_Y_POSTFIX = ''; // postfix for x values, eg ' kg'
  
    var POINT_NAME = 'district'; // point names that appear in tooltip
    var POINT_COLOR = 'rgba(0,0,255,0.7)'; // eg `black` or `rgba(10,100,44,0.8)`
    var POINT_RADIUS = 5; // radius of each data point
  
    var X_AXIS = 'Days to death'; // x-axis label, label in tooltip
    var Y_AXIS = 'Age at diagnosis (years)'; // y-axis label, label in tooltip
  
    var SHOW_GRID = true; // `true` to show the grid, `false` to hide
  
    // Read data file and create a chart
    $.get(dataurl, function(csvString) {
  
      var rows = Papa.parse(csvString, {header: true}).data;
  
      if (slug=='Colon'){
        var data = rows.map(function(row) {
          return {
            x: row[POINT_X]*360,
            y: row[POINT_Y],
            name: row[POINT_NAME]
          }
        })
    }else{
      var data = rows.map(function(row) {
        return {
          x: row[POINT_X],
          y: row[POINT_Y],
          name: row[POINT_NAME]
        }
      })
    }
      var scatterChartData = {
              datasets: [{
                  label: 'My First dataset',
                  backgroundColor: POINT_COLOR,
          data: data,
          pointRadius: POINT_RADIUS,
          pointHoverRadius:  POINT_RADIUS + 2,
              }]
      };
  
      var ctx = document.getElementById('scatterChart2').getContext('2d');
  
      var myScatterChart2 = new Chart.Scatter(ctx, {
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
                return [
                  X_AXIS + ': ' + POINT_X_PREFIX + tooltipItem.xLabel.toLocaleString() + POINT_X_POSTFIX,
                  Y_AXIS + ': ' + POINT_Y_PREFIX + tooltipItem.yLabel.toLocaleString() + POINT_Y_POSTFIX
                ]
              }
            }
          }
        }
      });
  
    });
  });