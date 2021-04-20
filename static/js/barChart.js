$(document).ready(function() {
  console.log(sense)
    if (sense=='reverse'){
        var TITLE = 'Top 100 opposite small molecule signatures';
    }else if (sense=='similar'){
        var TITLE = 'Top 100 similar small molecule signatures';
    }else if (sense=='gwas'){
        var TITLE = 'Top GWAS traits linked to input TFs';
    }else if (sense=='disease'){
        var TITLE = 'Top Human Phenotype Ontology terms linked to input TFs';
    }else if (sense=='tissueex'){
        var TITLE = 'Top tissues linked to input TFs by expression';
    }else if (sense=='tissuetar'){
        var TITLE = 'Top tissues linked to input TFs by targeting';
    }


  // `false` for vertical column chart, `true` for horizontal bar chart
  var HORIZONTAL = false;

	// `false` for individual bars, `true` for stacked bars
  var STACKED = false;  
  
  // Which column defines 'bucket' names?
  var LABELS = 'drug'; 
  if (sense=='gwas' || sense=='disease'){
    var LABELS = 'disease';  
  }else if (sense=='tissueex' || sense=='tissuetar'){
    var LABELS = 'tissue';  
  }

  if (sense=='reverse'){
      colors='#0f6efd'
  }else if (sense=='similar'){
      colors='#db3646'
  }else if (sense=='gwas'){
      colors='#db3646'
  }else if (sense=='disease'){
      colors='#db3646'
  }else if (sense=='tissueex'){
      colors='#28a744'
  }else if (sense=='tissuetar'){
      colors='#ffc107'
  }

  // For each column representing a data series, define its name and color
    var SERIES = [  
      {
        column: 'cosine',
        name: 'Cosine similarity',
        color: colors
      }
    ];
  if(sense=='gwas' || sense=='disease' || sense=='tissueex' || sense=='tissuetar'){
    var SERIES = [  
      {
        column: 'logpval',
        name: '-log(p-value)',
        color: colors
      }
    ];
  }

  // x-axis label and label in tooltip
  var X_AXIS = 'Small molecules';

  // y-axis label, label in tooltip
  var Y_AXIS = 'Cosine similarity';
  if(sense=='gwas'){
    // x-axis label and label in tooltip
    var X_AXIS = 'GWAS traits';

    // y-axis label, label in tooltip
    var Y_AXIS = '-log(p-value)';
  }else if(sense=='disease'){
      // x-axis label and label in tooltip
      var X_AXIS = 'Phenotype';

      // y-axis label, label in tooltip
      var Y_AXIS = '-log(p-value)';
  }else if(sense=='tissueex'){
      // x-axis label and label in tooltip
      var X_AXIS = 'Tissue';

      // y-axis label, label in tooltip
      var Y_AXIS = '-log(p-value)';
  }else if(sense=='tissuetar'){
      // x-axis label and label in tooltip
      var X_AXIS = 'Tissue';

      // y-axis label, label in tooltip
      var Y_AXIS = '-log(p-value)';
  }

  // `true` to show the grid, `false` to hide
  var SHOW_GRID = true; 

  // `true` to show the legend, `false` to hide
  var SHOW_LEGEND = false; 

  // Read data file and create a chart
 

    //var rows = Papa.parse(csvString, {header: true}).data;
    var rows=data2
    console.log(rows)

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

    //console.log(datasets)

    var canvasbar = document.getElementById('container');
    var ctx    = canvasbar.getContext('2d');

    var barchart = new Chart(ctx, {
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

        //datatables
        var table = $('#drugstbl1').DataTable({
          select:"single",
          columnDefs: [
            { orderable: false, targets: 0 },
                {
                    "targets": [ 7,8,9,10,11,12 ],
                    "visible": false,
                }
              ],
          "serverSide": false,
          "processing": true,
          "order": [[ 2, "desc" ]],
    
    
          buttons: [
                'copy', 'csv', 'pdf', 'print'
            ],
    
          "dom": "B" + "<'row'<'col-sm-12 col-md-6 mt-2'l><'col-sm-12 col-md-5'f>>" +
                 "<'row'<'col-sm-12'tr>>" +
                 "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        });
    
             // Add event listener for opening and closing details
        $('#drugstbl1 tbody').on('click', 'td.details-control', function () {
                 var tr = $(this).closest('tr');
                 var row = table.row(tr);
                 //console.log(row.data()[4])
    
                 if (row.child.isShown()) {
                     // This row is already open - close it
                     row.child.hide();
                     tr.find('svg').attr('color', 'green'); // FontAwesome 5
                     tr.find('svg').attr('data-icon', 'plus-circle');    // FontAwesome 5
                 }
                 else {
                     // Open this row
                     row.child(format(row.data())).show();
                     tr.find('svg').attr('color', 'red'); // FontAwesome 5
                     tr.find('svg').attr('data-icon', 'minus-circle'); // FontAwesome 5
                 }
             });
    
             table.on("user-select", function (e, dt, type, cell, originalEvent) {
                 if ($(cell.node()).hasClass("details-control")) {
                     e.preventDefault();
                 }
             });
    
    
             $('#drugstblcombin').on('click', 'tbody td', function() {
    
              //get textContent of the TD
              console.log('TD cell textContent : ', isNaN(Number(this.textContent))  )
              
              if (isNaN(Number(this.textContent))) {
                
                $('div.dataTables_filter input', table.table().container()).focus();
                table.search( this.textContent ).draw()
              }
    
              })

  //datatables
  var tablesim = $('#drugstbl2').DataTable({
    select:"single",
    columnDefs: [
      { orderable: false, targets: 0 },
          {
              "targets": [ 7,8,9,10,11,12 ],
              "visible": false,
          }
        ],
    "serverSide": false,
    "processing": true,
    "order": [[ 2, "desc" ]],


    buttons: [
          'copy', 'csv', 'pdf', 'print'
      ],

    "dom": "B" + "<'row'<'col-sm-12 col-md-6 mt-2'l><'col-sm-12 col-md-5'f>>" +
           "<'row'<'col-sm-12'tr>>" +
           "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
  });

       // Add event listener for opening and closing details
       $('#drugstbl2 tbody').on('click', 'td.details-control', function () {
           var tr = $(this).closest('tr');
           var row = tablesim.row(tr);
           //console.log(row.data()[4])

           if (row.child.isShown()) {
               // This row is already open - close it
               row.child.hide();
               tr.find('svg').attr('color', 'green'); // FontAwesome 5
               tr.find('svg').attr('data-icon', 'plus-circle');    // FontAwesome 5
           }
           else {
               // Open this row
               row.child(format(row.data())).show();
               tr.find('svg').attr('color', 'red'); // FontAwesome 5
               tr.find('svg').attr('data-icon', 'minus-circle'); // FontAwesome 5
           }
       });

       tablesim.on("user-select", function (e, dt, type, cell, originalEvent) {
           if ($(cell.node()).hasClass("details-control")) {
               e.preventDefault();
           }
       });

       $('#drugstblcombinsimilar').on('click', 'tbody td', function() {

        //get textContent of the TD
        console.log('TD cell textContent : ', isNaN(Number(this.textContent))  )

        if (isNaN(Number(this.textContent))) {
          
          $('div.dataTables_filter input', tablesim.table().container()).focus();
          tablesim.search( this.textContent ).draw()
            
        }

        })

    canvasbar.onclick = function(evt) {
      var activePoints = barchart.getElementsAtEvent(evt);
      if (activePoints[0]) {
        var label = activePoints[0]._view['label'];
        table.search(label).draw();
        tablesim.search(label).draw();
      }
    };


});
