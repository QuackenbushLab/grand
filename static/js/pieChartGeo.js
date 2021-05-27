$(document).ready(function() {
  
    // Read data file and create a chart
    $.get(dataurl2, function(csvString) {
  
      var rows = Papa.parse(csvString, {header: true}).data;

      var tablegeo= $('#tissuestablegeo').DataTable({
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

       $('#tissuestablegeo tfoot tr').appendTo('#tissuestablegeo thead');
       $("#tissuestablegeo").wrap("<div style='overflow:auto; width:100%;position:relative;'></div>");  

      if (slug == 'COAD'){
        var data = rows.map(function(row) {
            return row['gender'];
        })

        var dataETH = rows.map(function(row) {
            return row['race'];
        })

        var dataAL = rows.map(function(row) {
            return row['tumor_location'];
        })

        var dataStage = rows.map(function(row) {
            return row['uicc_stage'];
        })

        var dataVital = rows.map(function(row) {
            return row['vital_status'];
        })

        var text5='Anatomic location'
      }else if (slug == 'GBM'){
        var dataAL = rows.map(function(row) {
          return row['survival'];
        })
        var text5='Survival';
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

    var resultAL = foo(dataAL);
    if (slug == 'COAD'){
      var resultETH = foo(dataETH);
      var result = foo(data);
      var resultStage = foo(dataStage);//#dd979f
      var resultVital = foo(dataVital);
    }
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

    var pieChartDataAL2 = {
        labels: resultAL[0],
        datasets: [{
                data: resultAL[1],
                backgroundColor: colorArray.slice(0,resultAL[1].length-1),
                hoverBorderColor: colorArray.slice(0,resultAL[1].length-1)
              }]
      };

    if (slug == 'COAD'){
    var pieChartDataETH = {
        labels: resultETH[0],
        datasets: [{
          data: resultETH[1],
          backgroundColor: colorArray.slice(0,resultETH[1].length-1),
          hoverBorderColor: colorArray.slice(0,resultETH[1].length-1)
        }]
    };

    var pieChartData = {
        labels: result[0],
        datasets: [{
          data: result[1],
          backgroundColor: colorArray.slice(0,result[1].length-1),
          hoverBorderColor: colorArray.slice(0,result[1].length-1)
        }]
    };

    var pieChartDataStage2 = {
        labels: resultStage[0],
        datasets: [{
          data: resultStage[1],
          backgroundColor: colorArray.slice(0,resultStage[1].length-1),
          hoverBorderColor: colorArray.slice(0,resultStage[1].length-1)
        }]
    };

    var pieChartDataVital2 = {
        labels: resultVital[0],
        datasets: [{
          data: resultVital[1],
          backgroundColor: colorArray.slice(0,resultVital[1].length-1),
          hoverBorderColor: colorArray.slice(0,resultVital[1].length-1)
        }]
    };

  }


      var canvasAL2     = document.getElementById('myPieChartAL2');
      if (slug == 'COAD'){
        var canvasETH2  = document.getElementById('myPieChartETH2');
        var canvas2     = document.getElementById('myPieChart2');
        var canvasStage2= document.getElementById('myPieChartStage2');
        var canvasVital2= document.getElementById('myPieChartVital2');
      }
      var ctxAL2        = canvasAL2.getContext('2d');
      if (slug == 'COAD'){
        var ctxETH2      = canvasETH2.getContext('2d');
        var ctx2         = canvas2.getContext('2d');
        var ctxStage2    = canvasStage2.getContext('2d');
        var ctxVital2    = canvasVital2.getContext('2d');
      }

      var options = {
        backgroundColor: 'rgba(54, 162, 235,0.7)',
      }
  
      var myPieChartAL2 = new Chart(ctxAL2, {
        type: 'pie',
        data: pieChartDataAL2,
        options: {
            title: {
              display: true,
              text: text5,
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

      if (slug == 'COAD'){
      var myPieChart2 = new Chart(ctx2, {
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

    var myPieChartETH2 = new Chart(ctxETH2, {
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

    var myPieChartStage2 = new Chart(ctxStage2, {
        type: 'pie',
        data: pieChartDataStage2,
        options: {
            title: {
              display: true,
              text: 'Stage',
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

    var myPieChartVital2= new Chart(ctxVital2, {
        type: 'pie',
        data: pieChartDataVital2,
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
  }

  if (slug == 'COAD'){
    canvas2.onclick = function(evt) {
      var activePoints = myPieChart2.getElementsAtEvent(evt);
      if (activePoints[0]) {
        var chartData = activePoints[0]['_chart'].config.data;
        var idx = activePoints[0]['_index'];
  
        var label = chartData.labels[idx];
        tablegeo.column(1).search("^"+label+"$", true, false, true).draw();
        $("#id"+1+101+offset).val(label);
      }
    };

    canvasETH2.onclick = function(evt) {
        var activePoints = myPieChartETH2.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var chartData = activePoints[0]['_chart'].config.data;
          var idx = activePoints[0]['_index'];
    
          var label = chartData.labels[idx];
          tablegeo.column(2).search("^"+label+"$", true, false, true).draw();
          $("#id"+2+101+offset).val(label);
        }
      };

      canvasAL2.onclick = function(evt) {
        var activePoints = myPieChartAL2.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var chartData = activePoints[0]['_chart'].config.data;
          var idx = activePoints[0]['_index'];
    
          var label = chartData.labels[idx];
          tablegeo.column(5).search("^"+label+"$", true, false, true).draw();
          $("#id"+5+101+offset).val(label);
        }
      };

      canvasStage2.onclick = function(evt) {
        var activePoints = myPieChartStage2.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var chartData = activePoints[0]['_chart'].config.data;
          var idx = activePoints[0]['_index'];
    
          var label = chartData.labels[idx];
          tablegeo.column(6).search("^"+label+"$", true, false, true).draw();
          $("#id"+6+101+offset).val(label);
        }
      };

      canvasVital2.onclick = function(evt) {
        var activePoints = myPieChartVital2.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var chartData = activePoints[0]['_chart'].config.data;
          var idx = activePoints[0]['_index'];
    
          var label = chartData.labels[idx];
          tablegeo.column(8).search("^"+label+"$", true, false, true).draw();
          $("#id"+8+101+offset).val(label);
        }
      };
    }else if(slug == 'GBM'){

      canvasAL2.onclick = function(evt) {
        var activePoints = myPieChartAL2.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var chartData = activePoints[0]['_chart'].config.data;
          var idx = activePoints[0]['_index'];
    
          var label = chartData.labels[idx];
          tablegeo.column(1).search("^"+label+"$", true, false, true).draw();
          $("#id"+1+101+offset).val(label);
        }
      };


    }
    });
  });