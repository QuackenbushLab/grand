$(document).ready(function() {
  
    // Read data file and create a chart
  if(slug2 == 'lcl' || slug2=='fibroblast_gtex'){
    var rows=data2;
    console.log(rows)


    var data3 = rows.map(function(row) {
      return row.fields['gender'];
  })
  
  var dataETH = rows.map(function(row) {
      return row.fields['age'];
  })
  
  var dataAL = rows.map(function(row) {
    return row.fields['dthhrdy'];
})
  
  var dataStage = rows.map(function(row) {
    return row.fields['smatsscr'];
  })

  var dataVital = rows.map(function(row) {
    return row.fields['smtstptref'];
})
  var gbmtext3='Culture type'
  var gbmtext4='Autolysis score'



  function foo(arr) {
    var a = [], b = [], prev;
    
    arr.sort();
    for ( var i = 0; i < arr.length; i++ ) {
        if ( arr[i] !== prev ) {
            a.push(arr[i]);
            b.push(1);
        } else {
            b[b.length-1]++;
        }
        prev = arr[i];
    }
    
    return [a, b];
    }
    
    var result = foo(data3);
    var resultETH = foo(dataETH);
    var resultAL = foo(dataAL);
    var resultStage = foo(dataStage);
    var resultVital = foo(dataVital);
    var colorArray = ['#c6bebe', '#FFB399', '#78c186', '#e7f1ff', '#ba7fa5', 
    '#E6B333', '#7394e0', '#999966', '#99FF99', '#B34D4D',
    '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A', 
    '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
    '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC', 
    '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
    '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680', 
    '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
    '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3', 
    '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF'];
    
    var pieChartData = {
    labels: result[0],
    datasets: [{
            data: result[1],
            backgroundColor: colorArray.slice(0,result[1].length-1),
            hoverBorderColor: colorArray.slice(0,result[1].length-1)
          }]
    };
    
    
    var pieChartDataETH = {
    labels: resultETH[0],
    datasets: [{
      data: resultETH[1],
      backgroundColor: colorArray.slice(0,resultETH[1].length-1),
      hoverBorderColor: colorArray.slice(0,resultETH[1].length-1)
    }]
    };

    var pieChartDataAL = {
      labels: resultAL[0],
      datasets: [{
        data: resultAL[1],
        backgroundColor: colorArray.slice(0,resultAL[1].length-1),
        hoverBorderColor: colorArray.slice(0,resultAL[1].length-1)
      }]
      };

      var pieChartDataStage = {
        labels: resultStage[0],
        datasets: [{
          data: resultStage[1],
          backgroundColor: colorArray.slice(0,resultStage[1].length-1),
          hoverBorderColor: colorArray.slice(0,resultStage[1].length-1)
        }]
    };

    var pieChartDataVital = {
      labels: resultVital[0],
      datasets: [{
        data: resultVital[1],
        backgroundColor: colorArray.slice(0,resultVital[1].length-1),
        hoverBorderColor: colorArray.slice(0,resultVital[1].length-1)
      }]
      };

    var table = $('#tissuestable').DataTable({
      "serverSide": false,
      "processing": true,
      
       "dom": "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-5'>>" +
       "<'row'<'col-sm-12'tr>>" +
       "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
      
          initComplete: function () {
            // Apply the search
            this.api().columns().every( function () {
                var that = this;
      
                $( 'input', this.footer() ).on( 'keyup change clear', function () {
                    if ( that.search() !== this.value ) {
                        that
                        .search( this.value )
                        .draw();
                    }
                } );
            } );
        }
      });
      
      $('#tissuestable tfoot tr').appendTo('#tissuestable thead');

      var canvas     = document.getElementById('myPieChart');
      var canvasETH  = document.getElementById('myPieChartETH');
      var canvasStage   = document.getElementById('myPieChartStage');
      var canvasAL   = document.getElementById('myPieChartAL');
      var canvasVital= document.getElementById('myPieChartVital');
      var ctx        = canvas.getContext('2d');
      var ctxETH     = canvasETH.getContext('2d');
      var ctxAL      = canvasAL.getContext('2d');
      var ctxStage      = canvasStage.getContext('2d');
      var ctxVital   = canvasVital.getContext('2d');


      var options = {
        backgroundColor: 'rgba(54, 162, 235,0.7)',
        }
        
        var myPieChart = new Chart(ctx, {
        type: 'pie',
        data: pieChartData,
        options: {
            title: {
              display: true,
              text: 'Gender',
              fontSize: 10,
            },
            tooltips: {
                callbacks: {
                    title: function(tooltipItem, data) {
                        return data['labels'][tooltipItem[0]['index']];
                      },
                  label: function(tooltipItem, data) {
                    //get the concerned dataset
                    var dataset = data.datasets[tooltipItem.datasetIndex];
                    var currentValue = dataset.data[tooltipItem.index];
                    return currentValue;
                  }
                }
              },
            legend: {
                display: false
            } 
        }
        });
        
        var myPieChartETH = new Chart(ctxETH, {
        type: 'pie',
        data: pieChartDataETH,
        options: {
            title: {
              display: true,
              text: 'Age',
              fontSize: 10,
            },
            tooltips: {
                callbacks: {
                    title: function(tooltipItem, data) {
                        return data['labels'][tooltipItem[0]['index']];
                      },
                  label: function(tooltipItem, data) {
                    //get the concerned dataset
                    var dataset = data.datasets[tooltipItem.datasetIndex];
                    var currentValue = dataset.data[tooltipItem.index];
                    return currentValue;
                  }
                }
              },
            legend: {
                display: false
            } 
        }
        });

        var myPieChartAL = new Chart(ctxAL, {
          type: 'pie',
          data: pieChartDataAL,
          options: {
              title: {
                display: true,
                text: 'Hardy scale',
                fontSize: 10,
              },
              tooltips: {
                  callbacks: {
                      title: function(tooltipItem, data) {
                          return data['labels'][tooltipItem[0]['index']];
                        },
                    label: function(tooltipItem, data) {
                      //get the concerned dataset
                      var dataset = data.datasets[tooltipItem.datasetIndex];
                      var currentValue = dataset.data[tooltipItem.index];
                      return currentValue;
                    }
                  }
                },
              legend: {
                  display: false
              } 
          }
          });


          var myPieChartStage= new Chart(ctxStage, {
            type: 'pie',
            data: pieChartDataStage,
            options: {
                title: {
                  display: true,
                  text: gbmtext4,
                  fontSize: 10,
                },
                tooltips: {
                    callbacks: {
                        title: function(tooltipItem, data) {
                            return data['labels'][tooltipItem[0]['index']];
                          },
                      label: function(tooltipItem, data) {
                        //get the concerned dataset
                        var dataset = data.datasets[tooltipItem.datasetIndex];
                        var currentValue = dataset.data[tooltipItem.index];
                        return currentValue;
                      }
                    }
                  },
                legend: {
                    display: false
                } 
            }
        });

        var myPieChartVital= new Chart(ctxVital, {
          type: 'pie',
          data: pieChartDataVital,
          options: {
              title: {
                display: true,
                text: 'Time point',
                fontSize: 10,
              },
              tooltips: {
                  callbacks: {
                      title: function(tooltipItem, data) {
                          return data['labels'][tooltipItem[0]['index']];
                        },
                    label: function(tooltipItem, data) {
                      //get the concerned dataset
                      var dataset = data.datasets[tooltipItem.datasetIndex];
                      var currentValue = dataset.data[tooltipItem.index];
                      return currentValue;
                    }
                  }
                },
              legend: {
                  display: false
              } 
          }
          });

          canvas.onclick = function(evt) {
            var activePoints = myPieChart.getElementsAtEvent(evt);
            if (activePoints[0]) {
              var chartData = activePoints[0]['_chart'].config.data;
              var idx = activePoints[0]['_index'];
            
              var label = chartData.labels[idx];
              table.column(2).search("^"+label+"$", true, false, true).draw();
              $("#id"+2+offset).val(label);
            }
            };
            
            
            canvasETH.onclick = function(evt) {
            var activePoints = myPieChartETH.getElementsAtEvent(evt);
            if (activePoints[0]) {
              var chartData = activePoints[0]['_chart'].config.data;
              var idx = activePoints[0]['_index'];
            
              var label = chartData.labels[idx];
              table.column(3).search("^"+label+"$", true, false, true).draw();
              console.log("#id"+4+offset)
              $("#id"+3+offset).val(label);
            }
            };
            
            canvasAL.onclick = function(evt) {
            var activePoints = myPieChartAL.getElementsAtEvent(evt);
            if (activePoints[0]) {
              var chartData = activePoints[0]['_chart'].config.data;
              var idx = activePoints[0]['_index'];
            
              var label = chartData.labels[idx];
              table.column(4).search("^"+label+"$", true, false, true).draw();
              $("#id"+4+offset).val(label);
            }
            };

            canvasStage.onclick = function(evt) {
              var activePoints = myPieChartStage.getElementsAtEvent(evt);
              if (activePoints[0]) {
                var chartData = activePoints[0]['_chart'].config.data;
                var idx = activePoints[0]['_index'];
          
                var label = chartData.labels[idx];
                table.column(5).search("^"+label+"$", true, false, true).draw();
                $("#id"+5+offset).val(label);
              }
            };

            canvasVital.onclick = function(evt) {
              var activePoints = myPieChartVital.getElementsAtEvent(evt);
              if (activePoints[0]) {
                var chartData = activePoints[0]['_chart'].config.data;
                var idx = activePoints[0]['_index'];
              
                var label = chartData.labels[idx];
                table.column(10).search("^"+label+"$", true, false, true).draw();
                $("#id"+10+offset).val(label);
              }
              };

  }else{
  var rows=data2;
  console.log(rows)



var data3 = rows.map(function(row) {
    return row.fields['sex'];
})

var dataETH = rows.map(function(row) {
    return row.fields['race'];
})

var dataAL = rows.map(function(row) {
    return row.fields['culture'];
})

var dataStage = rows.map(function(row) {
    return row.fields['collsite'];
})

var dataVital = rows.map(function(row) {
    return row.fields['prim'];
})

var gbmtext3='Culture type'
var gbmtext4='Collection site'


function foo(arr) {
var a = [], b = [], prev;

arr.sort();
for ( var i = 0; i < arr.length; i++ ) {
    if ( arr[i] !== prev ) {
        a.push(arr[i]);
        b.push(1);
    } else {
        b[b.length-1]++;
    }
    prev = arr[i];
}

return [a, b];
}

var result = foo(data3);
var resultETH = foo(dataETH);
var resultAL = foo(dataAL);
var resultStage = foo(dataStage);
var resultVital = foo(dataVital);
var colorArray = ['#c6bebe', '#FFB399', '#78c186', '#e7f1ff', '#ba7fa5', 
'#E6B333', '#7394e0', '#999966', '#99FF99', '#B34D4D',
'#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A', 
'#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
'#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC', 
'#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
'#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680', 
'#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
'#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3', 
'#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF'];

var pieChartData = {
labels: result[0],
datasets: [{
        data: result[1],
        backgroundColor: colorArray.slice(0,result[1].length-1),
        hoverBorderColor: colorArray.slice(0,result[1].length-1)
      }]
};


var pieChartDataETH = {
labels: resultETH[0],
datasets: [{
  data: resultETH[1],
  backgroundColor: colorArray.slice(0,resultETH[1].length-1),
  hoverBorderColor: colorArray.slice(0,resultETH[1].length-1)
}]
};

var pieChartDataAL = {
labels: resultAL[0],
datasets: [{
  data: resultAL[1],
  backgroundColor: colorArray.slice(0,resultAL[1].length-1),
  hoverBorderColor: colorArray.slice(0,resultAL[1].length-1)
}]
};

var pieChartDataStage = {
labels: resultStage[0],
datasets: [{
  data: resultStage[1],
  backgroundColor: colorArray.slice(0,resultStage[1].length-1),
  hoverBorderColor: colorArray.slice(0,resultStage[1].length-1)
}]
};

var pieChartDataVital = {
labels: resultVital[0],
datasets: [{
  data: resultVital[1],
  backgroundColor: colorArray.slice(0,resultVital[1].length-1),
  hoverBorderColor: colorArray.slice(0,resultVital[1].length-1)
}]
};

var canvas     = document.getElementById('myPieChart');
var canvasETH  = document.getElementById('myPieChartETH');
var canvasAL   = document.getElementById('myPieChartAL');
var canvasStage= document.getElementById('myPieChartStage');
var canvasVital= document.getElementById('myPieChartVital');
var ctx        = canvas.getContext('2d');
var ctxETH     = canvasETH.getContext('2d');
var ctxAL      = canvasAL.getContext('2d');
var ctxStage   = canvasStage.getContext('2d');
var ctxVital   = canvasVital.getContext('2d');

console.log(offset)

var options = {
backgroundColor: 'rgba(54, 162, 235,0.7)',
}

var myPieChart = new Chart(ctx, {
type: 'pie',
data: pieChartData,
options: {
    title: {
      display: true,
      text: 'Sex',
      fontSize: 10,
    },
    tooltips: {
        callbacks: {
            title: function(tooltipItem, data) {
                return data['labels'][tooltipItem[0]['index']];
              },
          label: function(tooltipItem, data) {
            //get the concerned dataset
            var dataset = data.datasets[tooltipItem.datasetIndex];
            var currentValue = dataset.data[tooltipItem.index];
            return currentValue;
          }
        }
      },
    legend: {
        display: false
    } 
}
});

var myPieChartETH = new Chart(ctxETH, {
type: 'pie',
data: pieChartDataETH,
options: {
    title: {
      display: true,
      text: 'Race',
      fontSize: 10,
    },
    tooltips: {
        callbacks: {
            title: function(tooltipItem, data) {
                return data['labels'][tooltipItem[0]['index']];
              },
          label: function(tooltipItem, data) {
            //get the concerned dataset
            var dataset = data.datasets[tooltipItem.datasetIndex];
            var currentValue = dataset.data[tooltipItem.index];
            return currentValue;
          }
        }
      },
    legend: {
        display: false
    } 
}
});

var myPieChartAL = new Chart(ctxAL, {
type: 'pie',
data: pieChartDataAL,
options: {
    title: {
      display: true,
      text: gbmtext3,
      fontSize: 10,
    },
    tooltips: {
        callbacks: {
            title: function(tooltipItem, data) {
                return data['labels'][tooltipItem[0]['index']];
              },
          label: function(tooltipItem, data) {
            //get the concerned dataset
            var dataset = data.datasets[tooltipItem.datasetIndex];
            var currentValue = dataset.data[tooltipItem.index];
            return currentValue;
          }
        }
      },
    legend: {
        display: false
    } 
}
});

var myPieChartStage= new Chart(ctxStage, {
type: 'pie',
data: pieChartDataStage,
options: {
    title: {
      display: true,
      text: gbmtext4,
      fontSize: 10,
    },
    tooltips: {
        callbacks: {
            title: function(tooltipItem, data) {
                return data['labels'][tooltipItem[0]['index']];
              },
          label: function(tooltipItem, data) {
            //get the concerned dataset
            var dataset = data.datasets[tooltipItem.datasetIndex];
            var currentValue = dataset.data[tooltipItem.index];
            return currentValue;
          }
        }
      },
    legend: {
        display: false
    } 
}
});

var myPieChartVital= new Chart(ctxVital, {
type: 'pie',
data: pieChartDataVital,
options: {
    title: {
      display: true,
      text: 'Cancer type',
      fontSize: 10,
    },
    tooltips: {
        callbacks: {
            title: function(tooltipItem, data) {
                return data['labels'][tooltipItem[0]['index']];
              },
          label: function(tooltipItem, data) {
            //get the concerned dataset
            var dataset = data.datasets[tooltipItem.datasetIndex];
            var currentValue = dataset.data[tooltipItem.index];
            return currentValue;
          }
        }
      },
    legend: {
        display: false
    } 
}
});

var table = $('#tissuestable').DataTable({
"serverSide": false,
"processing": true,

 "dom": "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-5'>>" +
 "<'row'<'col-sm-12'tr>>" +
 "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",

    initComplete: function () {
      // Apply the search
      this.api().columns().every( function () {
          var that = this;

          $( 'input', this.footer() ).on( 'keyup change clear', function () {
              if ( that.search() !== this.value ) {
                  that
                  .search( this.value )
                  .draw();
              }
          } );
      } );
  }
});

$('#tissuestable tfoot tr').appendTo('#tissuestable thead');


canvas.onclick = function(evt) {
var activePoints = myPieChart.getElementsAtEvent(evt);
if (activePoints[0]) {
  var chartData = activePoints[0]['_chart'].config.data;
  var idx = activePoints[0]['_index'];

  var label = chartData.labels[idx];
  table.column(3).search("^"+label+"$", true, false, true).draw();
  $("#id"+3+offset).val(label);
}
};


canvasETH.onclick = function(evt) {
var activePoints = myPieChartETH.getElementsAtEvent(evt);
if (activePoints[0]) {
  var chartData = activePoints[0]['_chart'].config.data;
  var idx = activePoints[0]['_index'];

  var label = chartData.labels[idx];
  table.column(4).search("^"+label+"$", true, false, true).draw();
  console.log("#id"+4+offset)
  $("#id"+4+offset).val(label);
}
};

canvasAL.onclick = function(evt) {
var activePoints = myPieChartAL.getElementsAtEvent(evt);
if (activePoints[0]) {
  var chartData = activePoints[0]['_chart'].config.data;
  var idx = activePoints[0]['_index'];

  var label = chartData.labels[idx];
  table.column(5).search("^"+label+"$", true, false, true).draw();
  $("#id"+5+offset).val(label);
}
};

    canvasStage.onclick = function(evt) {
    var activePoints = myPieChartStage.getElementsAtEvent(evt);
    if (activePoints[0]) {
      var chartData = activePoints[0]['_chart'].config.data;
      var idx = activePoints[0]['_index'];

      var label = chartData.labels[idx];
      table.column(6).search("^"+label+"$", true, false, true).draw();
      $("#id"+6+offset).val(label);
    }
    };


    canvasVital.onclick = function(evt) {
    var activePoints = myPieChartVital.getElementsAtEvent(evt);
    if (activePoints[0]) {
      var chartData = activePoints[0]['_chart'].config.data;
      var idx = activePoints[0]['_index'];

      var label = chartData.labels[idx];
      table.column(7).search("^"+label+"$", true, false, true).draw();
      $("#id"+7+offset).val(label);
    }
    };

  }



});