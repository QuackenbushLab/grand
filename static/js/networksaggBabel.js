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
    nodes.push({
      id: 100006,
      x: x,
      y: y + 6*step,
      label: "Copy number",
      group: "cnv",
      value: 36,
      fixed: true,
      physics: false,
      font: { size: 24},
    });
    nodes.push({
      id: 100000,
      x: x,
      y: y + 0*step,
      label: "Methylation",
      group: "methyl",
      value: 36,
      fixed: true,
      physics: false,
      font: { size: 24},
    });
    nodes.push({
      id: 100007,
      x: x,
      y: y + 7*step,
      label: "Histone marks",
      group: "hm",
      value: 36,
      fixed: true,
      physics: false,
      font: { size: 24},
    });
    nodes.push({
      id: 100001,
      x: x,
      y: y + 1*step,
      label: "miRNA",
      group: "mir",
      value: 36,
      fixed: true,
      physics: false,
      font: { size: 24},
    });
    nodes.push({
      id: 100002,
      x: x,
      y: y + 2*step,
      label: "mRNA",
      group: "exp",
      value: 36,
      fixed: true,
      physics: false,
      font: { size: 24},
    });
    nodes.push({
      id: 100003,
      x: x,
      y: y + 3*step,
      label: "Protein",
      group: "prot",
      value: 36,
      fixed: true,
      physics: false,
      font: { size: 24},
    });
    nodes.push({
      id: 100004,
      x: x,
      y: y + 4*step,
      label: "Metabolite",
      group: "met",
      value: 36,
      fixed: true,
      physics: false,
      font: { size: 24},
    });
    nodes.push({
      id: 100005,
      x: x,
      y: y + 5*step,
      label: "Drug",
      group: "drugs",
      value: 36,
      fixed: true,
      physics: false,
      font: { size: 24},
    });
    nodes.push({
      id: 100008,
      x: x,
      y: y + 8*step,
      label: "Dependency",
      group: "dep",
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

      configure: {
        container: document.getElementById("config"),
        showButton: false,
      },

      groups: {
        methyl: {
          shape: "triangle",
          color: "#FF9900", // orange
        },
        exp: {
          shape: "dot",
          color: "#2B7CE9", // blue
        },
        prot: {
          shape: "dot",
          color: "#5A1E5C", // purple
        },
        mir: {
          shape: "square",
          color: "#C5000B", // red
        },
        met: {
          shape: "square",
          color: "#109618", // green
        },
        drugs: {
          shape: "star",
          color: "#103338", // green
        },
        cnv: {
          shape: "diamond",
          color: "#FB7E81", // green
        },
        hm: {
          shape: "box",
          color: "#97C2FC", // green
        },
        dep: {
          shape: "ellipse",
          color: "#6E6EFD", // green
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
      console.log(params.nodes)
      document.getElementById("selection").innerText =
        "Selection: " + nodes[params.nodes]['label'];
    });

  }
  //nodes[params.nodes]['label']
  window.addEventListener("load", () => {
    draw();
  });

});

