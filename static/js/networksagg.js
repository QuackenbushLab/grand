$(document).ready(function() {
  


    //$.each(rows.data, function(i) { //reduce to t tfs
    //    nodes2[i] = rows.data[i][""] ;
    //});

    //console.log(nodes);

    //var nodes = [
    //    { id: 0, label: "Myriel", group: 1 },
    //    { id: 1, label: "Napoleon", group: 1 },
    //    { id: 2, label: "Mlle.Baptistine", group: 2 },
    //  ];



function draw() {
    // create some nodes
    //var nodes = [
    //  { id: 0, label: "Myriel", group: 1 },
    //  { id: 1, label: "Napoleon", group: 1 },
    //  { id: 2, label: "Mlle.Baptistine", group: 1 },
    //];
        // Read data file and create a chart
        $.get(dataurl, function(csvString) {
  
            var rows = Papa.parse(csvString, 
              {
                  header: true,
                  delimiter: ",",
                  preview:10
              }
          );
      
      
          //console.log('Done!');
          var nodes = [];
      
          //var nodes = [];
          //var nodes2=[];
          $.each(rows.meta['fields'], function(i) { //reduce to n genes
              nodes[i] = {id:i, label: rows.meta['fields'][i], group: i};
              if(i === 2) {
                  return false; // breaks
              }
          });

  
    // create some edges
    var edges = [
      { from: 1, to: 0 },
      { from: 2, to: 0 },
      { from: 3, to: 0 },
    ];
  
    // create a network
    var container = document.getElementById("mynetwork");
    var data = {
      nodes: nodes,
      edges: edges,
    };
    var options = {
      nodes: {
        shape: "dot",
        size: 16,
      },
      physics: {
        forceAtlas2Based: {
          gravitationalConstant: -26,
          centralGravity: 0.005,
          springLength: 230,
          springConstant: 0.18,
        },
        maxVelocity: 146,
        solver: "forceAtlas2Based",
        timestep: 0.35,
        stabilization: { iterations: 150 },
      },
    };
    var network = new vis.Network(container, data, options);
});
  }
  

  window.addEventListener("load", () => {
    draw();
  });


});

