$(document).ready(function() {
console.log(slug)
if (slug2=='lcl' || slug2=='fibroblast_gtex'){
  var TITLE = 'Sample expression quality control 1: Mean coverage as a function of genes detected';  

  var POINT_X = 'smgnsdtc'; 

  var POINT_X_PREFIX = ''; // prefix for x values, eg '$'
  var POINT_X_POSTFIX = ''; // postfix for x values, eg '%'

  var POINT_Y = 'smmncpb'; 

  var POINT_Y_PREFIX = ''; // prefix for x values, eg 'USD '
  var POINT_Y_POSTFIX = ''; // postfix for x values, eg ' kg'

  var POINT_NAME = 'cleanname'; // point names that appear in tooltip

  var POINT_COLOR = 'rgba(54, 162, 235,0.7)'; // eg `black` or `rgba(10,100,44,0.8)`
  var POINT_RADIUS = 5; // radius of each data point

  var X_AXIS = 'Number of genes detected'; // x-axis label, label in tooltip
  var Y_AXIS = 'Mean coverage per base'; // y-axis label, label in tooltip

  var SHOW_GRID = true; // `true` to show the grid, `false` to hide
}else{
  var TITLE = 'Mutation rate as a function of doubling time';  

  var POINT_X = 'mutrate'; 

  var POINT_X_PREFIX = ''; // prefix for x values, eg '$'
  var POINT_X_POSTFIX = ''; // postfix for x values, eg '%'

  var POINT_Y = 'doublt'; 

  var POINT_Y_PREFIX = ''; // prefix for x values, eg 'USD '
  var POINT_Y_POSTFIX = ' hour'; // postfix for x values, eg ' kg'

  var POINT_NAME = 'depmap'; // point names that appear in tooltip

  var POINT_COLOR = 'rgba(54, 162, 235,0.7)'; // eg `black` or `rgba(10,100,44,0.8)`
  var POINT_RADIUS = 5; // radius of each data point

  var X_AXIS = 'Mutation rate'; // x-axis label, label in tooltip
  var Y_AXIS = 'Doubling time'; // y-axis label, label in tooltip

  var SHOW_GRID = true; // `true` to show the grid, `false` to hide
}
  // Read data file and create a chart


  var rows=data2;
  console.log(rows)
  colors='#0f6efd'

  var data = rows.map(function(row) {
    return {
      x: row.fields[POINT_X],
      y: row.fields[POINT_Y],
      name: row.fields[POINT_NAME]
    }
  })

  console.log(data);

  var scatterChartData = {
    datasets: [{
      label: 'height weight data',
      backgroundColor: POINT_COLOR,
      data: data,
      pointRadius: POINT_RADIUS,
      pointHoverRadius:  POINT_RADIUS + 2,
    }]
  };

  var canvas = document.getElementById('scatterChart');
  var ctx = canvas.getContext('2d');


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

  if (slug=='Adipose_subcutaneous_tissue' || slug=='Adipose_visceral_tissue' || slug=='Adrenal_gland_tissue' || slug=='Artery_aorta_tissue' || slug=='Artery_coronary_tissue' || slug=='Artery_tibial_tissue' || slug=='Brain_other_tissue' || slug=='Brain_cerebellum_tissue' || slug=='Brain_basal_ganglia_tissue' || slug=='Breast_tissue' || slug=='Colon_sigmoid_tissue' || slug=='Colon_transverse_tissue' || slug == 'Gastroesophageal_junction_tissue' || slug=='Esophagus_mucosa_tissue' || slug =='Esophagus_muscularis_tissue' || slug=='Heart_atrial_appendage_tissue' || slug=='Heart_left_ventricle_tissue' || slug=='Liver_tissue' || slug=='Lung_tissue' || slug=='Skeletal_muscle_tissue' || slug=='Tibial_nerve_tissue' || slug=='Pancreas_tissue' || slug=='Pituitary_tissue' || slug=='Skin_tissue' || slug=='Intestine_terminal_ileum_tissue' || slug=='Spleen_tissue' || slug=='Stomach_tissue' || slug=='Thyroid_tissue' || slug=='Whole_blood_tissue'){
        canvas.onclick = function(evt) {
          var activePoints = myScatterChart.getElementsAtEvent(evt);
          console.log(activePoints)
          if (activePoints[0]) {
            var idx = activePoints[0]['_index'];
            var label = activePoints[0]._chart.tooltip._data.datasets[0].data[idx]['name'];
            console.log(label)
            location.href = '/networks/aggregate/' + label
          }
        };
}

});

$(document).ready(function() {

  // Scatter chart 2

  if(slug2=='lcl' || slug2=='fibroblast_gtex'){
    var POINT_X = 'smrin'; 
    var POINT_Y = 'smtsisch'; 
  
    var TITLE = 'Sample expression quality control 2: Ischemic time as a function of RNA integrity';  

    var POINT_X_PREFIX = ''; // prefix for x values, eg '$'
    var POINT_X_POSTFIX = ''; // postfix for x values, eg '%'

    var POINT_Y_PREFIX = ''; // prefix for x values, eg 'USD '
    var POINT_Y_POSTFIX = ''; // postfix for x values, eg ' kg'

    var POINT_NAME = 'cleanname'; // point names that appear in tooltip

    var POINT_COLOR = '#475bfd'; // eg `black` or `rgba(10,100,44,0.8)`
    var POINT_RADIUS = 5; // radius of each data point

    var X_AXIS = 'RNA integrity number'; // x-axis label, label in tooltip
    var Y_AXIS = 'Total ischemic time'; // y-axis label, label in tooltip

    var SHOW_GRID = true; // `true` to show the grid, `false` to hide
  }else{
    var TITLE = 'Donor age and CAS9 activity';  

    var POINT_X = 'age'; 

    var POINT_X_PREFIX = ''; // prefix for x values, eg '$'
    var POINT_X_POSTFIX = ' years'; // postfix for x values, eg '%'

    var POINT_Y = 'cas9act'; 

    var POINT_Y_PREFIX = ''; // prefix for x values, eg 'USD '
    var POINT_Y_POSTFIX = ''; // postfix for x values, eg ' kg'

    var POINT_NAME = 'depmap'; // point names that appear in tooltip

    var POINT_COLOR = '#475bfd'; // eg `black` or `rgba(10,100,44,0.8)`
    var POINT_RADIUS = 5; // radius of each data point

    var X_AXIS = 'Age'; // x-axis label, label in tooltip
    var Y_AXIS = 'CAS9 activity'; // y-axis label, label in tooltip

    var SHOW_GRID = true; // `true` to show the grid, `false` to hide
  }
  // Read data file and create a chart


  var rows=data2;
  console.log(rows)
  colors='#475bfd'

  var data = rows.map(function(row) {
    return {
      x: row.fields[POINT_X],
      y: row.fields[POINT_Y],
      name: row.fields[POINT_NAME]
    }
  })

  console.log(data);

  var scatterChartData = {
    datasets: [{
      label: 'height weight data',
      backgroundColor: POINT_COLOR,
      data: data,
      pointRadius: POINT_RADIUS,
      pointHoverRadius:  POINT_RADIUS + 2,
    }]
  };

  var canvas = document.getElementById('scatterChart2');
  var ctx = canvas.getContext('2d');


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

  if (slug=='Adipose_subcutaneous_tissue' || slug=='Adipose_visceral_tissue' || slug=='Adrenal_gland_tissue' || slug=='Artery_aorta_tissue' || slug=='Artery_coronary_tissue' || slug=='Artery_tibial_tissue' || slug=='Brain_other_tissue' || slug=='Brain_cerebellum_tissue' || slug=='Brain_basal_ganglia_tissue' || slug=='Breast_tissue' || slug=='Colon_sigmoid_tissue' || slug=='Colon_transverse_tissue' || slug == 'Gastroesophageal_junction_tissue' || slug=='Esophagus_mucosa_tissue' || slug =='Esophagus_muscularis_tissue' || slug=='Heart_atrial_appendage_tissue' || slug=='Heart_left_ventricle_tissue' || slug=='Liver_tissue' || slug=='Lung_tissue' || slug=='Skeletal_muscle_tissue' || slug=='Tibial_nerve_tissue' || slug=='Pancreas_tissue' || slug=='Pituitary_tissue' || slug=='Skin_tissue' || slug=='Intestine_terminal_ileum_tissue' || slug=='Spleen_tissue' || slug=='Stomach_tissue' || slug=='Thyroid_tissue' || slug=='Whole_blood_tissue'){
      canvas.onclick = function(evt) {
        var activePoints = myScatterChart.getElementsAtEvent(evt);
        console.log(activePoints)
        if (activePoints[0]) {
          var idx = activePoints[0]['_index'];
          var label = activePoints[0]._chart.tooltip._data.datasets[0].data[idx]['name'];
          console.log(label)
          location.href = '/networks/aggregate/' + label
        }
      };
    }
});