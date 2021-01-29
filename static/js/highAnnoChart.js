var TITLE = 'Contribution of individual publications to GRAND networks';

// Caption underneath the chart
var CAPTION = 'Zoom in to see more annotations and click to get a link of the publication.';

// x-axis label and label in tooltip
var X_AXIS = 'Year';

// y-axis label and label in tooltip
var Y_AXIS = 'Number of networks';

// Should y-axis start from 0? `true` or `false`
var BEGIN_AT_ZERO = false;

// `true` to show the legend, `false` to hide
var SHOW_LEGEND = false;


$(document).ready(function() {

  // Read data file and create a chart
  $.get(dataurl, function(csvString) {

    var data = Papa.parse(csvString).data;
    var nSeries = data[0].length - 2

    var annotationPoints = data
      .filter(function(x) {return x[nSeries] !== ""})
      .map(function(x) {
        return {
          point: {
            xAxis: 0,
            yAxis: 0,
            x: x[0],
            y: x[1]
          },
          text: x[nSeries],
          url: x[nSeries+1],
        }
      })

    var series = []
    for (var i = 1; i <= nSeries; i++) {
      series.push({
        data: data.map(function(x) { return [parseFloat(x[0]), parseFloat(x[i])] }),
        name: data[0][i],
        marker: { enabled: false },
      })
    }

    // Now create the chart
    var myNewChart = Highcharts.chart('highcontainer', {

      chart: {
        type: 'line',
        zoomType: 'x',
        panning: true,
        panKey: 'shift',
        scrollablePlotArea: {
            minWidth: 600
        }
      },

      title: { text: TITLE },
      caption: { text: CAPTION },
      credits: { enabled: false },

      annotations: [{
        labelOptions: {
          backgroundColor: 'rgba(255,255,255,0.8)',
          verticalAlign: 'top',
          y: 10
        },
        labels: annotationPoints
      }],

      xAxis: {
        title: { text: X_AXIS },
      },

      yAxis: {
        startOnTick: true,
        min: BEGIN_AT_ZERO ? 0 : null,
        title: { text: Y_AXIS },
        labels: { formatter: function(x) {return x.value.toLocaleString()} }
      },

      legend: { enabled: SHOW_LEGEND },

      series: series,

      plotOptions: {
        series: {
            cursor: 'pointer',
            point: {
                events: {
                    click: function() {
                      location.href = this.series.chart.annotations[0].options.labels[this.index-1].url;
                    }
                }
            }
        }
        },

    });

  });

});