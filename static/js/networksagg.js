$(document).ready(function() {
  //var nodes = null;
  //var edges = null;
  var network = null;
  
  function destroy() {
    if (network !== null) {
      network.destroy();
      network = null;
    }
  }

  function draw() {
    destroy();
    // create people.
    // value corresponds with the age of the person
    //nodes = [
    //  { id: 1, label: "Algie" },
    //  { id: 2, label: "Alston" },
     // { id: 3, label: "Barney" },
     // { id: 4, label: "Coley" },
     // { id: 5, label: "Grant" },
     // { id: 6, label: "Langdon" },
     // { id: 7, label: "Lee" },
     // { id: 8, label: "Merlin" },
     // { id: 9, label: "Mick" },
    //  { id: 10, label: "Tod" },
    //];
  
    // create connections between people
    // value corresponds with the amount of contact between two people
    //edges = [
    //  { from: 2, to: 8, value: 3 },
    //  { from: 2, to: 9, value: 5 },
    //  { from: 2, to: 10, value: 1 },
    //  { from: 4, to: 6, value: 8 },
    //  { from: 5, to: 7, value: 2 },
    //  { from: 4, to: 5, value: 1 },
    //  { from: 9, to: 10, value: 2 },
    //  { from: 2, to: 3, value: 6 },
    //  { from: 3, to: 9, value: 4 },
    //  { from: 5, to: 3, value: 1 },
    //  { from: 2, to: 7, value: 4 },
    //];
  
    // Instantiate our network object.
    var container = document.getElementById("mynetwork");

    var x = -container.clientWidth +50 ;
    var y = -container.clientHeight / 2 + 50;
    var step = 170;

    if (slug.substr(-4) == 'PUMA' || slug == 'mirnadragon'){
    nodes.push({
      id: 1003,
      x: x,
      y: y,
      label: "miRNA",
      group: "mir",
      value: 36,
      fixed: true,
      physics: false,
      font: { size: 24},
    });
  }else{
    nodes.push({
      id: 1003,
      x: x,
      y: y,
      label: "TF",
      group: "tf",
      value: 36,
      fixed: true,
      physics: false,
      font: { size: 24},
    });
  }
    nodes.push({
      id: 1004,
      x: x,
      y: y + step,
      label: "Gene",
      group: "exp",
      value: 36,
      fixed: true,
      physics: false,
      font: { size: 24},
    });

    var data = {
      nodes: nodes,
      edges: edges,
    };
    var options = {
      nodes: {
        shape: "dot",
        scaling: {
          min: 10,
          max: 30,
        },
        font: {
          size: 8,
          face: "Helvetica",
        },
      },
      edges: {
        width: 0.15,
        smooth: {
          type: "continuous",
        },
      },
      interaction: {
        navigationButtons: true,
        keyboard: true,
      },
      autoResize: true,

      configure: {
        container: document.getElementById("config"),
        showButton: false,
      },
      groups: {
        exp: {
          shape: "dot",
          color: "#d7cad1", // blue
        },

        mir: {
          shape: "square",
          color: "#C5000B", // red
        },
        tf: {
          shape: "triangle",
          color: "#98c4e1", // green
        },
      },
      //configure: {
      //  filter: function (option, path) {
      //    if (option === "type" && path.indexOf("smooth") !== -1) {
      //      return true;
      //    }
      //    if (option === "roundness") {
      //      return true;
      //    }
      //    if (path.indexOf("hierarchical") !== -1) {
      //      return true;
      //    }
      //    return false;
      //  },
      //  container: document.getElementById("optionsContainer"),
      //  showButton: false,
      //},
      physics: true,
    };


    
    network = new vis.Network(container, data, options);
    


    network.on("select", function (params) {
      document.getElementById("selection").innerText =
        "Selection: " + nodes[params.nodes]['label'];
    });

    network.on("afterDrawing", function (ctx) {
      var dataURL = ctx.canvas.toDataURL();
      document.getElementById('mynetwork').src = dataURL;
      //network.fit();
    });

  }


  
  var button = document.getElementById('btn-download');
  button.addEventListener('click', function (e) {
      var dataURL = document.getElementById('mynetwork').src;
      button.href = dataURL;

  });

  window.addEventListener("load", () => {
    draw();
  });



});

