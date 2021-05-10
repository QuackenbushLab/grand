$(document).ready(function() {
  
    // Read data file and create a chart
    $.get(dataurl3, function(csvString) {
  
      var rows = Papa.parse(csvString, {header: true}).data;

      if (slug == 'COAD'){
        var data2 = rows.map(function(row) {
            return row['gender'];
        })

        var dataETH = rows.map(function(row) {
            return row['race'];
        })

        var dataAL = rows.map(function(row) {
            return row['anatomic_neoplasm_subdivision'];
        })

        var dataStage = rows.map(function(row) {
            return row['uicc_stage'];
        })

        var dataVital = rows.map(function(row) {
            return row['vital_status'];
        })
    }else if (slug == 'GBM'){
      var data2 = rows.map(function(row) {
        return row['gender'];
      })

      var dataETH = rows.map(function(row) {
          return row['race'];
      })

      var dataAL = rows.map(function(row) {
          return row['neoadjuvanttherapy'];
      })

      var dataStage = rows.map(function(row) {
          return row['radiationsradiationregimenindication'];
      })

      var dataVital = rows.map(function(row) {
          return row['vitalstatus'];
      })

      var gbmtext3='Neoadjuvant therapy'
      var gbmtext4='Radiotherapy'

    }else{
        var data2 = rows.map(function(row) {
            return row['gdc_cases.demographic.gender'];
        })

        var dataETH = rows.map(function(row) {
            return row['gdc_cases.demographic.race'];
        })

        var dataAL = rows.map(function(row) {
            return row['gdc_cases.project.primary_site'];
        })

        var dataStage = rows.map(function(row) {
            return row['gdc_cases.diagnoses.tumor_stage'];
        })

        var dataVital = rows.map(function(row) {
            return row['gdc_cases.diagnoses.vital_status'];
        })
    }
  
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

    var result = foo(data2);
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

      var canvas     = document.getElementById('myPieChart22');
      var canvasETH  = document.getElementById('myPieChartETH22');
      var canvasAL   = document.getElementById('myPieChartAL22');
      var canvasStage= document.getElementById('myPieChartStage22');
      var canvasVital= document.getElementById('myPieChartVital22');
      var ctx        = canvas.getContext('2d');
      var ctxETH     = canvasETH.getContext('2d');
      var ctxAL      = canvasAL.getContext('2d');
      var ctxStage   = canvasStage.getContext('2d');
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
              text: 'Vital status',
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

    var table = $('#tissuestabletcga22').DataTable({
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

    $('#tissuestabletcga22 tfoot tr').appendTo('#tissuestabletcga22 thead');
       
    if (slug == 'GBM') {
      canvas.onclick = function(evt) {
        var activePoints = myPieChart.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var chartData = activePoints[0]['_chart'].config.data;
          var idx = activePoints[0]['_index'];
    
          var label = chartData.labels[idx];
          table.column(1).search("^"+label+"$", true, false, true).draw();
          $("#id"+1+100+offset).val(label);
        }
      };


    canvasETH.onclick = function(evt) {
        var activePoints = myPieChartETH.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var chartData = activePoints[0]['_chart'].config.data;
          var idx = activePoints[0]['_index'];
    
          var label = chartData.labels[idx];
          table.column(2).search("^"+label+"$", true, false, true).draw();
          $("#id"+2+100+offset).val(label);
        }
      };

      canvasAL.onclick = function(evt) {
        var activePoints = myPieChartAL.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var chartData = activePoints[0]['_chart'].config.data;
          var idx = activePoints[0]['_index'];
    
          var label = chartData.labels[idx];
          table.column(7).search("^"+label+"$", true, false, true).draw();
          $("#id"+7+100+offset).val(label);
        }
      };

      canvasStage.onclick = function(evt) {
        var activePoints = myPieChartStage.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var chartData = activePoints[0]['_chart'].config.data;
          var idx = activePoints[0]['_index'];
    
          var label = chartData.labels[idx];
          table.column(8).search("^"+label+"$", true, false, true).draw();
          $("#id"+8+100+offset).val(label);
        }
      };

      canvasVital.onclick = function(evt) {
        var activePoints = myPieChartVital.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var chartData = activePoints[0]['_chart'].config.data;
          var idx = activePoints[0]['_index'];
    
          var label = chartData.labels[idx];
          table.column(9).search("^"+label+"$", true, false, true).draw();
          $("#id"+9+100+offset).val(label);
        }
      };


    }else{
      canvas.onclick = function(evt) {
        var activePoints = myPieChart.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var chartData = activePoints[0]['_chart'].config.data;
          var idx = activePoints[0]['_index'];
    
          var label = chartData.labels[idx];
          table.column(1).search("^"+label+"$", true, false, true).draw();
          $("#id"+1+offset).val(label);
        }
      };


    canvasETH.onclick = function(evt) {
        var activePoints = myPieChartETH.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var chartData = activePoints[0]['_chart'].config.data;
          var idx = activePoints[0]['_index'];
    
          var label = chartData.labels[idx];
          table.column(2).search("^"+label+"$", true, false, true).draw();
          console.log("#id"+2+offset)
          $("#id"+2+offset).val(label);
        }
      };

      canvasAL.onclick = function(evt) {
        var activePoints = myPieChartAL.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var chartData = activePoints[0]['_chart'].config.data;
          var idx = activePoints[0]['_index'];
    
          var label = chartData.labels[idx];
          table.column(6).search("^"+label+"$", true, false, true).draw();
          $("#id"+6+offset).val(label);
        }
      };

      canvasStage.onclick = function(evt) {
        var activePoints = myPieChartStage.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var chartData = activePoints[0]['_chart'].config.data;
          var idx = activePoints[0]['_index'];
    
          var label = chartData.labels[idx];
          table.column(7).search("^"+label+"$", true, false, true).draw();
          $("#id"+7+offset).val(label);
        }
      };

      canvasVital.onclick = function(evt) {
        var activePoints = myPieChartVital.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var chartData = activePoints[0]['_chart'].config.data;
          var idx = activePoints[0]['_index'];
    
          var label = chartData.labels[idx];
          table.column(9).search("^"+label+"$", true, false, true).draw();
          $("#id"+9+offset).val(label);
        }
      };

    }
  
    });

  });