$(document).ready(function() {
  
    // Read data file and create a chart
    $.get(dataurl, function(csvString) {
  
      var rows = Papa.parse(csvString, {header: true}).data;

      if (slug == 'Colon'){
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
    var resultStage = foo(dataStage);//#dd979f
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
              datasets: [{
                data: result[1],
                backgroundColor: colorArray.slice(0,result[1].length-1),
                hoverBorderColor: colorArray.slice(0,result[1].length-1)
              }],
              //labels: result[0]
      };

  
    var pieChartDataETH = {
        datasets: [{
          data: resultETH[1],
          backgroundColor: colorArray.slice(0,resultETH[1].length-1),
          hoverBorderColor: colorArray.slice(0,resultETH[1].length-1)
        }],
        //labels: resultETH[0]
    };

    var pieChartDataAL = {
        datasets: [{
          data: resultAL[1],
          backgroundColor: colorArray.slice(0,resultAL[1].length-1),
          hoverBorderColor: colorArray.slice(0,resultAL[1].length-1)
        }],
        //labels: resultETH[0]
    };

    var pieChartDataStage = {
        datasets: [{
          data: resultStage[1],
          backgroundColor: colorArray.slice(0,resultStage[1].length-1),
          hoverBorderColor: colorArray.slice(0,resultStage[1].length-1)
        }],
        //labels: resultETH[0]
    };

      var ctx = document.getElementById('myPieChart').getContext('2d');
      var ctxETH = document.getElementById('myPieChartETH').getContext('2d');
      var ctxAL = document.getElementById('myPieChartAL').getContext('2d');
      var ctxStage = document.getElementById('myPieChartStage').getContext('2d');

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
        }
    });

    var myPieChart = new Chart(ctxETH, {
        type: 'pie',
        data: pieChartDataETH,
        options: {
            title: {
              display: true,
              text: 'Race',
              fontSize: 10,
            },
        }
    });

    var myPieChart = new Chart(ctxAL, {
        type: 'pie',
        data: pieChartDataAL,
        options: {
            title: {
              display: true,
              text: 'Anatomic location',
              fontSize: 10,
            },
        }
    });

    var myPieChart = new Chart(ctxStage, {
        type: 'pie',
        data: pieChartDataStage,
        options: {
            title: {
              display: true,
              text: 'Stage',
              fontSize: 10,
            },
        }
    });
  
    });
  });