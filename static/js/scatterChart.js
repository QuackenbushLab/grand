$(document).ready(function() {

  if (slug == 'BRCA'){
    var TITLE = 'Sample quality control';
  }else if (slug == 'GBM'){
    var TITLE = 'Relationship between survival and performance score';
  }else{
    var TITLE = 'Height and weight at diagnosis';  
  }

  if (slug == 'COAD'){
    var POINT_X = 'height_cm_at_diagnosis'; // column name for x values in data.csv
  }else if (slug == 'BRCA'){
    var POINT_X = 'cgc_slide_percent_tumor_nuclei'; 
  }else if (slug == 'GBM'){
    var POINT_X = 'karnofskyperformancescore';
  }else if (slug == 'PAAD'){
    var POINT_X = 'subtype';
  }else{
    var POINT_X = 'gdc_cases.exposures.height'; 
  }
  var POINT_X_PREFIX = ''; // prefix for x values, eg '$'
  var POINT_X_POSTFIX = ''; // postfix for x values, eg '%'

  if (slug == 'COAD'){
    var POINT_Y = 'weight_kg_at_diagnosis'; // column name for y values in data.csv
  }else if (slug == 'BRCA'){
    var POINT_Y = 'cgc_slide_percent_necrosis';   
  }else if (slug == 'GBM'){
    var POINT_Y = 'daystodeath';   
  }else if (slug == 'PAAD'){
    var POINT_Y = 'gdc_cases.diagnoses.days_to_death';
  }else{
    var POINT_Y = 'gdc_cases.exposures.weight'; 
  }

  var POINT_Y_PREFIX = ''; // prefix for x values, eg 'USD '
  var POINT_Y_POSTFIX = ''; // postfix for x values, eg ' kg'

  var POINT_NAME = 'sample'; // point names that appear in tooltip
  if (slug == 'CESC' || slug == 'BRCA' || slug == 'LIHC' || slug == 'PAAD'){
    var POINT_NAME = 'gdc_cases.samples.portions.analytes.aliquots.submitter_id'; // point names that appear in tooltip
  }else if (slug == 'GBM'){
    var POINT_NAME = 'submitter_id';
  }
  var POINT_COLOR = 'rgba(54, 162, 235,0.7)'; // eg `black` or `rgba(10,100,44,0.8)`
  var POINT_RADIUS = 5; // radius of each data point

  if (slug == 'BRCA'){
    var X_AXIS = 'Tumor nuclei in sample (%)'; // x-axis label, label in tooltip
    var Y_AXIS = 'Necrosis in sample (%) '; // y-axis label, label in tooltip
  }else if (slug == 'GBM'){
    var X_AXIS = 'Karnofsky performance score'; // x-axis label, label in tooltip
    var Y_AXIS = 'Days to death'; // y-axis label, label in tooltip
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

    if( slug == 'PAAD' ){
      var data2 = rows.map(function(row) {
        return {
          x: row[POINT_X],
          y: row['cgc_case_age_at_diagnosis'],
          name: row[POINT_NAME]
        }
      })
      function averageFemale(list) {
        var sum1 = 0,
            count1 = 0,
            sum2 = 0,
            count2 = 0,
            i;
    
        for (i = 0; i < list.length; i++) {
            if (list[i].x === '1') {
              if(list[i].y != 'NA'){
                sum1 += Number(list[i].y);
                ++count1;
              }
            }else if(list[i].x === '2') {
              if(list[i].y != 'NA'){
                sum2 += Number(list[i].y);
                ++count2;
              }
            }
        }
        return [sum1 / count1, sum2 / count2];
       }   
      var barData = averageFemale(data)
      var barData2 = averageFemale(data2)
    }else{
      var scatterChartData = {
        datasets: [{
          label: 'height weight data',
          backgroundColor: POINT_COLOR,
          data: data,
          pointRadius: POINT_RADIUS,
          pointHoverRadius:  POINT_RADIUS + 2,
        }]
      };
  }

    var canvas = document.getElementById('scatterChart')
    var ctx = canvas.getContext('2d');

    if( slug == 'PAAD'){
      var canvas = document.getElementById('scatterChartPancreas2');
      var ctx2 = canvas.getContext('2d');
      var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Basal-like', 'Classical'],
            datasets: [{
                label: 'Average survival ',
                data: barData,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
          title: {
            display: true,
            text: 'Average survival and subtype',
            fontSize: 14,
          },
            legend: {
              display: false
          },
          scales: {
            xAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Subtype'
              },
              gridLines: {
                display: SHOW_GRID,
              }
            }],
            yAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Average survival (Days)'
              },
              gridLines: {
                display: SHOW_GRID,
              },
              ticks: {
                beginAtZero: true
            }
            }]
          }
        }
    });
    var myChart2 = new Chart(ctx2, {
      type: 'bar',
      data: {
          labels: ['Basal-like', 'Classical'],
          datasets: [{
              label: 'Average age ',
              data: barData2,
              backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 0.2)'
              ],
              borderColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)'
              ],
              borderWidth: 1
          }]
      },
      options: {
        title: {
          display: true,
          text: 'Average age and subtype',
          fontSize: 14,
        },
          legend: {
            display: false
        },
        scales: {
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Subtype'
            },
            gridLines: {
              display: SHOW_GRID,
            }
          }],
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Average age (Years)'
            },
            gridLines: {
              display: SHOW_GRID,
            },
            ticks: {
              beginAtZero: true
          }
          }]
        }
      }
    });


    }else{
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


    // PAAD
    if (slug == 'PAAD' || slug == 'GBM' || slug == 'COAD'){
      canvas.onclick = function(evt) {
        var activePoints = myScatterChart.getElementsAtEvent(evt);
        console.log(activePoints)
        if (activePoints[0]) {
          var idx = activePoints[0]['_index'];
          var label = activePoints[0]._chart.tooltip._data.datasets[0].data[idx]['name'];
          //console.log(label.replaceAll('-','_'))
          location.href = '/networks/aggregate/'+ slug +'_1_' + label.replaceAll('-','_')
        }
      };
  }

  }

  });



  
});


$(document).ready(function() {

    if (slug == 'GBM'){
        var TITLE = 'Days to death and age at diagnosis';
    }else{
        var TITLE = 'Relationship between survival and age';
    }
    if (slug == 'COAD'){
      var POINT_X = 'time_to_event'; // column name for x values in data.csv
    }else if (slug == 'GBM'){
      var POINT_X = 'yearstobirth'; 
    }else{
      var POINT_X = 'gdc_cases.diagnoses.days_to_death'; // column name for x values in data.csv
    }
    var POINT_X_PREFIX = ''; // prefix for x values, eg '$'
    var POINT_X_POSTFIX = ''; // postfix for x values, eg '%'
  
    if (slug == 'COAD'){
      var POINT_Y = 'age_at_initial_pathologic_diagnosis'; // column name for y values in data.csv
    }else if (slug == 'GBM'){
      var POINT_Y = 'daystodeath'; 
    }else{
      var POINT_Y = 'cgc_case_age_at_diagnosis'; // column name for y values in data.csv
    }
    var POINT_Y_PREFIX = ''; // prefix for x values, eg 'USD '
    var POINT_Y_POSTFIX = ''; // postfix for x values, eg ' kg'
  
    var POINT_NAME = 'sample'; // point names that appear in tooltip
    if (slug == 'CESC' || slug == 'BRCA' || slug == 'LIHC' || slug == 'PAAD'){
      var POINT_NAME = 'gdc_cases.samples.portions.analytes.aliquots.submitter_id'; // point names that appear in tooltip
    }else if (slug == 'GBM'){
      var POINT_NAME = 'submitter_id';
    }
    var POINT_COLOR = 'rgba(0,0,255,0.7)'; // eg `black` or `rgba(10,100,44,0.8)`
    var POINT_RADIUS = 5; // radius of each data point
  
    if (slug == 'GBM'){
      var X_AXIS = 'Days to death'; // x-axis label, label in tooltip
      var Y_AXIS = 'Age at diagnosis (years)'; // y-axis label, label in tooltip
    }else{
      var Y_AXIS = 'Age at diagnosis (years)'; // x-axis label, label in tooltip
      var X_AXIS = 'Days to death'; // y-axis label, label in tooltip
    }
  
    var SHOW_GRID = true; // `true` to show the grid, `false` to hide
  
    // Read data file and create a chart
    $.get(dataurl, function(csvString) {
  
      var rows = Papa.parse(csvString, {header: true}).data;
  
      if (slug=='COAD'){
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
  
      var canvas = document.getElementById('scatterChart2')
      var ctx = canvas.getContext('2d');
  
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


      if (slug == 'PAAD' || slug == 'GBM' || slug == 'COAD'){
        canvas.onclick = function(evt) {
          var activePoints = myScatterChart2.getElementsAtEvent(evt);
          console.log(activePoints)
          if (activePoints[0]) {
            var idx = activePoints[0]['_index'];
            var label = activePoints[0]._chart.tooltip._data.datasets[0].data[idx]['name'];
            //console.log(label.replaceAll('-','_'))
            location.href = '/networks/aggregate/'+ slug +'_1_' + label.replaceAll('-','_')
          }
        };
  }
  
    });
  });