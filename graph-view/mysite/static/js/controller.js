/**
 * Created by shamsabz on 3/2/21.
 */

var graphType = 0;
var circleSliderValue = 1100;
var nodeSliderValue = 15;
var fontSliderValue = 20;
var widthSliderValue = 1500;
var network = JSON.parse('{}');
var ptm2ab = JSON.parse('{}');
var fileName = "initial";
$("#chartGE").hide();
$("#chartColor").hide();

function convertToCSV(objArray) {
    var array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;
    var str = '';

    for (var i = 0; i < array.length; i++) {
        var line = '';
        for (var index in array[i]) {
            if (line != '') line += ','

            line += array[i][index];
        }

        str += line + '\r\n';
    }

    return str;
}

function computeNetworkFromInputJson(input_f) {

    var nodes = [];
    //==============================================
    var edges = [];
    //==============================================
    var nodesUnique = {};
    //==============================================
    var newNode = {};
    //==============================================
    var newEdge = {};

    var network_f = {};
    //log.info(mapping.toString());
//        log.info("here");
//         String gene;
//         String pathway;
//         Double relation;
    var idx = 0;
    // int tag1, tag2, edgeId;


    for(i = 0; i < input_f.length; i++) {
        //JSONObject inputItem = (JSONObject) input.get(i);
        var tag1 = 1;
        var tag2 = 1;
        var edgeId = 1;

        var gene = input_f[i]["Category1"];
        var pathway = input_f[i]["Category2"];
        var relation = input_f[i]["Relation"];
        if ('Category1Id' in input_f[i]){
            tag1 = input_f[i]["Category1Id"];
        }

        if ('Category2Id' in input_f[i]){
            tag2 = input_f[i]["Category2Id"];
        }

        if ('EdgeId' in input_f[i]){
            edgeId = input_f[i]["EdgeId"];
        }


        // System.out.println(gene);
        // System.out.println(pathway);
        // System.out.println(relation);

//            log.info(gene);
//            log.info(pathway);
        if(tag1 != -1) {
            if (!(gene in nodesUnique)) {
                newNode = generateNode(gene, idx, tag1);
                //idx = idx + 1;
                idx = idx + 1;
                nodesUnique[gene] = newNode;
                nodes.push(nodesUnique[gene]);
            }
        }
        if(tag2 != -1) {
            if (!(pathway in nodesUnique)) {
                newNode = generateNode(pathway, idx, tag2);
                //idx = idx + 1;
                idx = idx + 1;
                nodesUnique[pathway] = newNode;
                nodes.push(nodesUnique[pathway]);
            }
        }
//                newEdgeNode = new JSONObject();
//                newEdgeNode.put("source", newGeneNode.get("idx"));
//                newEdgeNode.put("target", ((JSONObject) KEGG2013Unique.get(pathway)).get("idx"));//["idx"];//.get(pathway));
        if(tag2 != -1 && tag2 != -1) {
            newEdge = generateEdgeNode(nodesUnique[gene]["idx"], nodesUnique[pathway]["idx"], relation, edgeId);
            edges.push(newEdge);
        }


    }

    network_f["nodes"] = nodes;
    network_f["edges"] = edges;


    return network_f;
}



function generateEdgeNode(sourceTag, targetTag, value, edgeId)
{
    var node = {};
    node["source"] = sourceTag;
    node["target"] = targetTag;
    node["weight"] = value;
    node["tag"] = edgeId;
    //node.put("value", 1);
    //node.put("weight", 1);
    return node;
}



function generateNode(name, idx, tag)//, float center, int value)
{
    var node = {};
//        Random random = new Random();
//        double rand = random.nextDouble();
//        double scaled = rand * 400;
    if (name.length > 33) {
        node["name"] = name.substring(0, 30) + "...";
    }else{
        node["name"] = name;
    }

    node["full_name"] = name;
    node["idx"] = idx;
    //node.put("px", center + scaled);
    //node.put("x", center + scaled);
    //rand = random.nextDouble();
    //scaled = rand * 200;
    //node.put("y", center + scaled);
    //node.put("py", center + scaled);
    //node.put("value",value);
    node["group"] = tag;
    node["weight"] = 0;

    return node;
}


function exportCSVFile(headers, items, fileTitle) {
    console.log(items);
    if (headers) {
        items.unshift(headers);
    }
    console.log(items);
    // Convert Object to JSON
    var jsonObject = JSON.stringify(items);
    console.log(jsonObject);
    var csv = convertToCSV(jsonObject);

    var exportedFilenmae = fileTitle + '.csv' || 'export.csv';

    var blob = new Blob([csv], {type: 'text/csv;charset=utf-8;'});
    if (navigator.msSaveBlob) { // IE 10+
        navigator.msSaveBlob(blob, exportedFilenmae);
    } else {
        var link = document.createElement("a");
        if (link.download !== undefined) { // feature detection
            // Browsers that support HTML5 download attribute
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", exportedFilenmae);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
}


$(document).ready(function () {

    $('#download_link2').click(function () {
        console.log("clicked1");
        d3.csv('/static/example/graph_illustration2.csv', function (data) {

            console.log(data);
            var itemsFormatted = [];
            var headers = {
                Category1: 'Category1'.replace(/,/g, ''), // remove commas to avoid errors
                Category2: "Category2",
                Relation: "Relation",
                Category1Id: "Category1Id",
                Category2Id: "Category2Id",
                EdgeId: "EdgeId"
            };
            var itemsNotFormatted = data;
            itemsNotFormatted.forEach(function (item) {
                itemsFormatted.push({
                    Category1: item.Category1.replace(/,/g, ''), // remove commas to avoid errors,
                    Category2: item.Category2.replace(/,/g, ''),
                    Relation: item.Relation.replace(/,/g, ''),
                    Category1Id: item.Category1Id.replace(/,/g, ''),
                    Category2Id: item.Category2Id.replace(/,/g, ''),
                    EdgeId: item.EdgeId.replace(/,/g, '')

                });
            });

            var fileTitle = 'pinet_graph_illustration'; // or 'my-unique-title'

            exportCSVFile(headers, itemsFormatted, fileTitle); // call the exportCSVFile() function to process the JSON and trigger the download

        })
    });
});


$(document).ready(function () {

    $('#download_link1').click(function () {
        console.log("clicked1");
        d3.csv('/static/example/graph_illustration.csv', function (data) {

            console.log(data);
            var itemsFormatted = [];
            var headers = {
                Category1: 'Category1'.replace(/,/g, ''), // remove commas to avoid errors
                Category2: "Category2",
                Relation: "Relation",
                Category1Id: "Category1Id",
                Category2Id: "Category2Id",
                EdgeId: "EdgeId"
            };
            var itemsNotFormatted = data;
            itemsNotFormatted.forEach(function (item) {
                itemsFormatted.push({
                    Category1: item.Category1.replace(/,/g, ''), // remove commas to avoid errors,
                    Category2: item.Category2.replace(/,/g, ''),
                    Relation: item.Relation.replace(/,/g, ''),
                    Category1Id: item.Category1Id.replace(/,/g, ''),
                    Category2Id: item.Category2Id.replace(/,/g, ''),
                    EdgeId: item.EdgeId.replace(/,/g, '')

                });
            });

            var fileTitle = 'pinet_graph_illustration_node_ordered'; // or 'my-unique-title'

            exportCSVFile(headers, itemsFormatted, fileTitle); // call the exportCSVFile() function to process the JSON and trigger the download

        })
    });
});


$(function () {

    $(".js-upload-upload4").click(function () {
        console.log("4 clicked");
        $("#fileupload4").click();
    });

    $("#fileupload4").fileupload({
        dataType: 'json',
        done: function (e, data) {
            if (data.result.is_valid) {
                console.log(data);
                $("#gallery tbody").prepend(
                    "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
                )

            }
        }
    });

});




$(document).on('input', '#circle_slider', function () {
    $('#circle_slider_value').html($(this).val());
////console.log($(this).val());
    circleSliderValue = $(this).val();


    makeGEGraph(network, ptm2ab, fileName, fontSliderValue, widthSliderValue, circleSliderValue, nodeSliderValue, graphType);
});

$(document).on('input', '#node_slider', function () {
    $('#node_slider_value').html($(this).val());
////console.log($(this).val());
    nodeSliderValue = $(this).val();

    makeGEGraph(network, ptm2ab, fileName, fontSliderValue, widthSliderValue, circleSliderValue, nodeSliderValue, graphType);


});

$(document).on('input', '#font_slider', function () {
    $('#font_slider_value').html($(this).val());
////console.log($(this).val());
    fontSliderValue = $(this).val();

    makeGEGraph(network, ptm2ab, fileName, fontSliderValue, widthSliderValue, circleSliderValue, nodeSliderValue, graphType);
});

$(document).on('input', '#width_slider', function () {
    $('#width_slider_value').html($(this).val());
////console.log($(this).val());
    widthSliderValue = $(this).val();

    makeGEGraph(network, ptm2ab, fileName, fontSliderValue, widthSliderValue, circleSliderValue, nodeSliderValue, graphType);
});

//
// $('#file-upload-form').on('sumbit', function(){
//     console.log("inside myform");
//     var form = $(this);
//     var formdata = false;
//     if (window.FormData){
//         formdata = new FormData(form[0]);
//     }
//
//     var formAction = form.attr('action');
//     $.ajax({
//         url         : '/upload',
//         data        : formdata ? formdata : form.serialize(),
//         cache       : false,
//         contentType : false,
//         processData : false,
//         type        : 'POST',
//         success     : function(data, textStatus, jqXHR){
//             // Callback code
//         }
//     });
// });
//
//
//
//
// $('#uploadFileGraph').click(function() {
//     console.log("inside uploadFileGraph");
//
// self.uploadGraphWaiting = true;
// //self.showGEGraph = false;
// var file = $scope.myFileCSV;
// var fd = new FormData();
// self.uploadWaiting = true;
// self.showOutput = false;
// self.interest ="";
// fd.append('file', file);
// var fileName = String(file.name).slice(0, -4).concat(String(self.interest));
// console.log(fileName);
//
// //We can send anything in name parameter,
// //it is hard coded to abc as it is irrelavant in this case.
// var uploadUrl = "api/uploadCSV";
//
// $http.post(uploadUrl, fd, {
//     transformRequest: angular.identity,
//     headers: {'Content-Type': undefined}
// })
//     .success(function(response){
//         console.log(response);
//         var pNetwork = response;
//         var ptmToAbundance = {};
//         for (var iterNetNode = 0; iterNetNode < pNetwork.nodes.length; iterNetNode++)
//         {
//             //pNetwork.nodes[iterNetNode]["weight"] = 0;
//             var iterNetNodeKey = pNetwork.nodes[iterNetNode]["name"];
//             ptmToAbundance[iterNetNodeKey] = "NA";
//             // if (iterNetNodeKey in ptmToAbundance)
//             // {
//             //     //console.log(iterNetNodeKey);
//             //     if (ptmToAbundance[iterNetNodeKey] == "NA")
//             //     {
//             //         pNetwork.nodes[iterNetNode]["value"] = 0.0;
//             //     }
//             //     else {
//             //         pNetwork.nodes[iterNetNode]["value"] = ptmToAbundance[iterNetNodeKey];
//             //     }
//             // }
//         }
//
//         $scope.makeGEGraph(response, ptmToAbundance, fileName, $scope.fontSliderValue, $scope.widthSliderValue, $scope.circleSliderValue, $scope.nodeSliderValue, self.graphType);
//         self.uploadGraphWaiting = false;
//         self.showGEGraph = true;
//     })
//     .error(function(response){
//         self.uploadGraphWaiting = false;
//         self.showGEGraph = true;
//     });
// })
$(function () {

    $(".js-upload-upload1").click(function () {
        console.log("1 clicked");

        $("#fileupload1").click();
    });

    $("#fileupload1").fileupload({
        dataType: 'json',
        done: function (e, data) {
            if (data.result.is_valid) {

                console.log(data);
                console.log(data.result.url);
                fileName = data.result.name;
                d3.csv(data.result.url, function (data) {

                    //console.log(data);
                    var itemsFormatted = [];
                    var headers = {
                        Category1: 'Category1'.replace(/,/g, ''), // remove commas to avoid errors
                        Category2: "Category2",
                        Relation: "Relation",
                        Category1Id: "Category1Id",
                        Category2Id: "Category2Id",
                        EdgeId: "EdgeId"
                    };
                    var itemsNotFormatted = data;
                    itemsNotFormatted.forEach(function (item) {
                        itemsFormatted.push({
                            Category1: item.Category1.replace(/,/g, ''), // remove commas to avoid errors,
                            Category2: item.Category2.replace(/,/g, ''),
                            Relation: item.Relation.replace(/,/g, ''),
                            Category1Id: item.Category1Id.replace(/,/g, ''),
                            Category2Id: item.Category2Id.replace(/,/g, ''),
                            EdgeId: item.EdgeId.replace(/,/g, '')

                        });
                    });
console.log(itemsFormatted);
network = computeNetworkFromInputJson(itemsFormatted);
              ptm2ab = JSON.parse('{}');
                    //makeGEGraph(network, ptm2ab, "foo", 12, 1400, 900, 5, 1);
                    makeGEGraph(network, ptm2ab, fileName, fontSliderValue, widthSliderValue, circleSliderValue, nodeSliderValue, graphType);


                })
                $("#gallery tbody").prepend(
                    "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
                )

            }
        }
    });

});


function makeGEGraph(input_network, ptmToAbundance, fileName, fontSize, widthSize, circleSize, nodeSize, graphType) {
//console.log(self.computeWeightForUpdatePtm);


    $("#chartGE").show();
$("#chartColor").show();
    d3.select("#chartGE").select("svg").remove();
    if (typeof svgGE === 'undefined') {
        var svgGE = d3.selectAll("#chartGE").append("svg");
    }
//var svg4 = d3.selectAll("#chart4").append("svg");


    var force;
    var colNodeScaleSeparate = d3.scale.ordinal()
        .range(["#987024", "#ed0909", "#0af702", "#d506d8"])
        //.range(["#987024", "#982482", "#0af702"])
        .domain([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]);
//#f9a3f5
// var colNodeScaleSeparate = d3.scale.ordinal()
//     .range(["#767776", "#f91104", "#0af702"])
//     .domain([0,1,2]);

// var colNodeScale = d3.scale.linear().range(["#987024", "#ed0909"]);
// var colScale = d3.scale.linear().range(["#987024", "#ed0909"]);

    var colScale = d3.scale.ordinal()
        .range(["#987024", "#ed0909", "#0af702", "#d506d8"])
        //.range(["#987024", "#982482", "#0af702"])
        .domain([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]);

    var colNodeScale = d3.scale.ordinal()
        .range(["#987024", "#ed0909", "#0af702", "#d506d8"])
        //.range(["#987024", "#982482", "#0af702"])
        .domain([1, 2, 3, 4]);
    var edgeWeightScale = d3.scale.linear().range([1, 3]);
    var xScale = d3.scale.linear().range([nodeSize / 3.0, nodeSize]);
    var scoreScale = d3.scale.linear().range([1.0, 3.0]).domain([0.0, 1.0]);
    var textPlacePlusMinus = d3.scale.ordinal()
        .range([18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18])
        .domain([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]);
    var textPlaceStartEnd = d3.scale.ordinal().range(["end", "end", "end", "end", "end", "end", "end", "end", "end", "end", "end", "end", "end", "end", "end", "end", "end", "end", "end", "end", "end", "end", "end", "end"])
        .domain([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]);

    var colorsForAbundance = ["#00A6FF", "#1097E0", "#2885B7", "#35799E", "#4C7991", "#6D828D", "#8C8C8C", "#8E8E5C", "#92923C", "#A5A52E", "#BDBD24", "#DDDD15", "#FFFF00"];
    var domain_data = [-2.0, -1.6, -1.2, -0.8, -0.4, -0.01, 0.01, 0.4, 0.8, 1.2, 1.6, 2.0, 1000];
    var colorScale = d3.scale.threshold()
        .domain(domain_data)
        .range(colorsForAbundance);


    function updateGE(nodes, links, fontSize, widthSize, circleSize, nodeSize) {

        circleSize = Math.min(circleSize, widthSize - 300);
        console.log("in updateGE");
        console.log(nodes);
        console.log(links);
        //
        //var svg;


        // $('force1').click();
        //document.getElementById('force1').click();

        // //console.log(circularLayout);


        // self.computeWeightForupdatePtm = false;
        // SharedService.setVar('computeWeightForupdatePtm', self.computeWeightForupdatePtm);


        // Set-up the export button
        // d3.select('#download-png').on('click', function() {
        //
        // })
        function circularViewGE() {
            svgGE.remove();

            xScale.domain(d3.extent(nodes, function (d) {
                return d.weight;
            }));
            scoreScale.domain(d3.extent(links, function (d) {
                return d.weight;
            }));
            colNodeScale.domain(d3.extent(nodes, function (d) {
                return d.group;
            }));
            colScale.domain(d3.extent(links, function (d) {
                return d.weight;
            }));
            var margin = 75,
                w = widthSize - 2 * margin,
                h = w,
                radius = w / 2,
                strokeWidth = 4,
                hyp2 = Math.pow(radius, 2),
                nodeBaseRad = 5;


            globalH = h;
            globalHPlus50 = h + 50;
            globalW = w;


            svgGE = d3.select("#chartGE")
                .append("svg")
                .attr("style", "outline: thin solid yellow;")
                .attr("width", w)
                .attr("height", globalHPlus50);
            svgGE.append("rect")
                .attr("width", "100%")
                .attr("height", "100%")
                .attr("fill", "white");


            // This is for grouping nodes


            var force = d3.layout.force()
                .nodes(nodes)
                .links(links)
                .size([w, h]);

// evenly spaces nodes along arc
            var circleCoord = function (node, index, input_num_nodes, has_focus) {
                //console.log("in circleCoord");

                // console.log(node["name"]);
                // console.log(index);
                // String(node["name"]).valueOf() ==
                var circumference = circle.node().getTotalLength();
                var pointAtLength = function (l) {
                    return circle.node().getPointAtLength(l)
                };


                if (has_focus) {
                    var added_num = parseInt(input_num_nodes / 4);
                    if (added_num % 2 == 1) {
                        added_num += 1;
                    }
                    var num_nodes = input_num_nodes + added_num;
                    var sectionLength = (circumference) / num_nodes;
                    if (String(node["name"]).valueOf() === self.interest) {
                        var position = 0;
                        // console.log("in ATP");
                        // console.log(pointAtLength(circumference - position));
                        // console.log(position);
                    }
                    else {


                        var position = sectionLength * (index + added_num / 2) + sectionLength / 2;
                    }
                }
                else {
                    var num_nodes = input_num_nodes;
                    var sectionLength = (circumference) / num_nodes;
                    var position = sectionLength * (index) + sectionLength / 2;

                }

                //console.log(pointAtLength(circumference - position));
                return pointAtLength(circumference - position)
            }

            var is_connected = function (d, opacity) {
                lines.transition().style("stroke-opacity", function (o) {
                    return o.source === d || o.target === d ? 1 : opacity;
                });
            }

            var is_connected_on_click = function (d, opacity) {
                //console.log(d);
                lines.transition().style("stroke-opacity", function (o) {
                    return o.source.group === d.group || o.target.group === d.group ? 1 : opacity;
                });
            }
            // var dim = w - 900
            // var circle = svgGE.append("path")
            //     .attr("d", "M 450, " + (dim / 2 + 450) + " a " + dim / 2 + "," + dim / 2 + " 0 1,0 " + dim + ",0 a " + dim / 2 + "," + dim / 2 + " 0 1,0 " + dim * -1 + ",0")
            //     .style("fill", "white");

            var dim = w - (widthSize - circleSize)
            var circle = svgGE.append("path")
                .attr("d", "M " + String((widthSize - circleSize) / 2) + ", " + (dim / 2 + (widthSize - circleSize) / 2) + " a " + dim / 2 + "," + dim / 2 + " 0 1,0 " + dim + ",0 a " + dim / 2 + "," + dim / 2 + " 0 1,0 " + dim * -1 + ",0")
                .style("fill", "white");

            force.start();
            var has_focus = false;
            nodes.forEach(function (n, i) {
                if (String(n["name"]).valueOf() == self.interest) {
                    //if (String(n["name"]).valueOf() === $scope.interest) {
                    has_focus = true;
                }

            })
            nodes.forEach(function (n, i) {
                var coord = circleCoord(n, i, nodes.length, has_focus)
                n.x = coord.x
                n.y = coord.y
            });


            // use this one for straight line links...
            // var lines = svg.selectAll("line.node-link")
            //     .data(links).enter().append("line")
            //     .attr("class", "node-link")
            //     .attr("x1", function(d) { return d.source.x; })
            //     .attr("y1", function(d) { return d.source.y; })
            //     .attr("x2", function(d) { return d.target.x; })
            //     .attr("y2", function(d) { return d.target.y; });

            var lines = svgGE.selectAll("path.node-link")
                .data(links).enter().append("path")
                .style("fill", "none")
                .style("stroke", function (d) {

                    if (d.tag == 0) {
                        return ("#696969");
                    }
                    else if (d.tag == 1) {
                        return ("#006400");
                    }
                    else if (d.tag == 2) {
                        return ("#00FF00");
                    }
                    else if (d.tag == 3) {
                        return ("#0000FF");
                    }
                    else if (d.tag == 4) {
                        return ("#808080");
                    }
                    else if (d.tag == 5) {
                        return ("#8B4513");
                    }
                    else if (d.tag == 6) {
                        return ("#FFFFE0");
                    }
                    else if (d.tag == 7) {
                        return ("#8464c5");
                    }
                    else if (d.tag == 8) {
                        return ("#00FFFF");
                    }
                    else if (d.tag == 9) {
                        return ("#FF7F50");
                    }
                    else if (d.tag == 10) {
                        return ("#FF0000");
                    }
                    else if (d.tag == 11) {
                        return ("#FF00FF");
                    }
                    else if (d.tag == 12) {
                        return ("#8FBC8F");
                    }
                    else if (d.tag == 13) {
                        return ("#A52A2A");
                    }
                    else if (d.tag == 14) {
                        return ("#FFD700");
                    }
                    else if (d.tag == 15) {
                        return ("#A0522D");
                    }
                    else if (d.tag == 16) {
                        return ("#FFFF00");
                    }
                    else if (d.tag == 17) {
                        return ("#6A5ACD");
                    }
                    else if (d.tag == 18) {
                        return ("#708090");
                    }
                    else if (d.tag == 19) {
                        return ("#FF6347");
                    }
                    else if (d.tag == 20) {
                        return ("#CD5C5C");
                    }
                    else if (d.tag == 21) {
                        return ("#DB7093");
                    }
                    else if (d.tag == 22) {
                        return ("#2E8B57");
                    }
                    else if (d.tag == 23) {
                        return ("#000080");
                    }
                    else if (d.tag == 24) {
                        return ("#9370DB");
                    }
                    else if (d.tag == 25) {
                        return ("#A52A2A");
                    }
                    else if (d.tag == 26) {
                        return ("#FDF5E6");
                    }
                    else if (d.tag == 27) {
                        return ("#7B68EE");
                    }
                    else if (d.tag == 28) {
                        return ("#696969");
                    }
                    else if (d.tag == 29) {
                        return ("#FF4500");
                    }
                    else if (d.tag == 30) {
                        return ("#DC143C");
                    }
                    else if (d.tag == 31) {
                        return ("#FF69B4");
                    }
                    else if (d.tag == 32) {
                        return ("#006400");
                    }
                    else if (d.tag == 33) {
                        return ("#87CEEB");
                    }
                    else if (d.tag == 34) {
                        return ("#EE82EE");
                    }
                    else if (d.tag == 35) {
                        return ("#800000");
                    }
                    else if (d.tag == 36) {
                        return ("#FAEBD7");
                    }
                    else if (d.tag == 37) {
                        return ("#4B0082");
                    }
                    else if (d.tag == 38) {
                        return ("#808080");
                    }
                    else if (d.tag == 39) {
                        return ("#FF8C00");
                    }
                    else if (d.tag == 40) {
                        return ("#FA8072");
                    }
                    else if (d.tag == 41) {
                        return ("#FFC0CB");
                    }
                    else if (d.tag == 42) {
                        return ("#9ACD32");
                    }
                    else if (d.tag == 43) {
                        return ("#4682B4");
                    }
                    else if (d.tag == 44) {
                        return ("#DDA0DD");
                    }
                    else if (d.tag == 45) {
                        return ("#CD853F");
                    }
                    else if (d.tag == 46) {
                        return ("#FFE4E1");
                    }
                    else if (d.tag == 47) {
                        return ("#696969");
                    }
                    else if (d.tag == 48) {
                        return ("#A9A9A9");
                    }
                    else if (d.tag == 49) {
                        return ("#FFA500");
                    }
                    else {
                        return ("#000000");
                    }


                    // if (d.group == 0) {
                    //     return colorScale(d.value);
                    // }
                    // else {
                    //
                    //     if (d.group == 1) {
                    //         return("#ed0909");
                    //     }
                    //     if (d.group == 2) {
                    //         return("#0af702");
                    //     }
                    //     if (d.group == 3) {
                    //         return("#FF00FF");
                    //     }
                    //     if (d.group == 4) {
                    //         return("#808000");
                    //     }
                    //     if (d.group == 5) {
                    //         return("#000080");
                    //     }
                    //     if (d.group == 6) {
                    //         return("#800080");
                    //     }
                    //     if (d.group == 7) {
                    //         return("#00ffff");
                    //     }
                    //     if (d.group == 8) {
                    //         return("#F5F5DC");
                    //     }
                    //     if (d.group == 9) {
                    //         return("#A52A2A");
                    //     }
                    //     if (d.group == 10) {
                    //         return("#8B0000");
                    //     }
                    //     if (d.group == 11) {
                    //         return("#FF8C00");
                    //     }
                    //
                    // }

                })
                //.style("stroke", "#726363")
                .attr("class", "node-link")
                .style("stroke-width", function (d) {
                    return scoreScale(d.weight);
                })
                .attr("d", function (d) {

                    //
                    // var dx = d.target.x - d.source.x,
                    //     dy = d.target.y - d.source.y,
                    //     dr = Math.sqrt(dx * dx + dy * dy),
                    //     a1 = dx,
                    //     a2 = dy,
                    //     b1 = w/2 - d.source.x,
                    //     b2 = h/2 - d.source.y,
                    //
                    //     drx = dr/1.5,
                    //     dry = dr/1.5,
                    //     xRotation = 0, // degrees
                    //     largeArc = 0, // 1 or 0
                    //
                    //     sweep = 1, // 1 or 0
                    //     x2 = d.target.x,
                    //     y2 = d.target.y;
                    // if( (a1*b2 - a2*b1) > 0)
                    // {
                    //     sweep = 0
                    // }
                    // else
                    // {sweep = 1}
                    //
                    //
                    // return "M" + d.source.x + "," + d.source.y + "A" + drx + "," + dry + " " + xRotation + "," + largeArc + "," + sweep + " " + x2 + "," + y2;
                    //
                    //


                    var dx = d.target.x - d.source.x,
                        dy = d.target.y - d.source.y,
                        dr = Math.sqrt(dx * dx + dy * dy);
                    return "M" +
                        d.source.x + "," +
                        d.source.y + "," +
                        d.target.x + "," +
                        d.target.y;

                });


            var gnodes = svgGE.selectAll('g.gnode')
                .data(nodes).enter().append('g')
                .attr("transform", function (d) {
                    return "translate(" + d.x + "," + d.y + ")"
                })
                .classed('gnode', true);


            // node.append("circle")
            //     .attr("r", function (d) { return xScale(d.weight); })
            //     .style("fill", function(d) { return colNodeScale(d.group); });

            var node = gnodes.append("circle")
                .attr("r", function (d) {
                    return xScale((d.weight));
                })
                .style("fill", function (d) {

                    if (d.group == 0) {
                        return ("#696969");
                    }
                    else if (d.group == 1) {
                        return ("#006400");
                    }
                    else if (d.group == 2) {
                        return ("#00FF00");
                    }
                    else if (d.group == 3) {
                        return ("#0000FF");
                    }
                    else if (d.group == 4) {
                        return ("#808080");
                    }
                    else if (d.group == 5) {
                        return ("#8B4513");
                    }
                    else if (d.group == 6) {
                        return ("#FFFFE0");
                    }
                    else if (d.group == 7) {
                        return ("#8464c5");
                    }
                    else if (d.group == 8) {
                        return ("#00FFFF");
                    }
                    else if (d.group == 9) {
                        return ("#FF7F50");
                    }
                    else if (d.group == 10) {
                        return ("#FF0000");
                    }
                    else if (d.group == 11) {
                        return ("#FF00FF");
                    }
                    else if (d.group == 12) {
                        return ("#8FBC8F");
                    }
                    else if (d.group == 13) {
                        return ("#A52A2A");
                    }
                    else if (d.group == 14) {
                        return ("#FFD700");
                    }
                    else if (d.group == 15) {
                        return ("#A0522D");
                    }
                    else if (d.group == 16) {
                        return ("#FFFF00");
                    }
                    else if (d.group == 17) {
                        return ("#6A5ACD");
                    }
                    else if (d.group == 18) {
                        return ("#708090");
                    }
                    else if (d.group == 19) {
                        return ("#FF6347");
                    }
                    else if (d.group == 20) {
                        return ("#CD5C5C");
                    }
                    else if (d.group == 21) {
                        return ("#DB7093");
                    }
                    else if (d.group == 22) {
                        return ("#2E8B57");
                    }
                    else if (d.group == 23) {
                        return ("#000080");
                    }
                    else if (d.group == 24) {
                        return ("#9370DB");
                    }
                    else if (d.group == 25) {
                        return ("#A52A2A");
                    }
                    else if (d.group == 26) {
                        return ("#FDF5E6");
                    }
                    else if (d.group == 27) {
                        return ("#7B68EE");
                    }
                    else if (d.group == 28) {
                        return ("#696969");
                    }
                    else if (d.group == 29) {
                        return ("#FF4500");
                    }
                    else if (d.group == 30) {
                        return ("#DC143C");
                    }
                    else if (d.group == 31) {
                        return ("#FF69B4");
                    }
                    else if (d.group == 32) {
                        return ("#006400");
                    }
                    else if (d.group == 33) {
                        return ("#87CEEB");
                    }
                    else if (d.group == 34) {
                        return ("#EE82EE");
                    }
                    else if (d.group == 35) {
                        return ("#800000");
                    }
                    else if (d.group == 36) {
                        return ("#FAEBD7");
                    }
                    else if (d.group == 37) {
                        return ("#4B0082");
                    }
                    else if (d.group == 38) {
                        return ("#808080");
                    }
                    else if (d.group == 39) {
                        return ("#FF8C00");
                    }
                    else if (d.group == 40) {
                        return ("#FA8072");
                    }
                    else if (d.group == 41) {
                        return ("#FFC0CB");
                    }
                    else if (d.group == 42) {
                        return ("#9ACD32");
                    }
                    else if (d.group == 43) {
                        return ("#4682B4");
                    }
                    else if (d.group == 44) {
                        return ("#DDA0DD");
                    }
                    else if (d.group == 45) {
                        return ("#CD853F");
                    }
                    else if (d.group == 46) {
                        return ("#FFE4E1");
                    }
                    else if (d.group == 47) {
                        return ("#696969");
                    }
                    else if (d.group == 48) {
                        return ("#A9A9A9");
                    }
                    else if (d.group == 49) {
                        return ("#FFA500");
                    }

                    else if (d.group == 117) {
                        return ("#FFD600FF");
                    }
                    else if (d.group == 64) {
                        return ("#FF7600FF");
                    }
                    else if (d.group == 85) {
                        return ("#FFFF9CFF");
                    }
                    else if (d.group == 95) {
                        return ("#FF3000FF");
                    }
                    else if (d.group == 123) {
                        return ("#FFFF0BFF");
                    }
                    else if (d.group == 88) {
                        return ("#FFFFF1FF");
                    }
                    else if (d.group == 73) {
                        return ("#FFC800FF");
                    }
                    else if (d.group == 118) {
                        return ("#FFDD00FF");
                    }
                    else if (d.group == 129) {
                        return ("#FFFF8AFF");
                    }
                    else if (d.group == 54) {
                        return ("#FF1B00FF");
                    }
                    else if (d.group == 122) {
                        return ("#FFF800FF");
                    }
                    else if (d.group == 130) {
                        return ("#FFFF9FFF");
                    }
                    else if (d.group == 99) {
                        return ("#FF5300FF");
                    }
                    else if (d.group == 98) {
                        return ("#FF4C00FF");
                    }
                    else if (d.group == 56) {
                        return ("#FF2E00FF");
                    }
                    else if (d.group == 89) {
                        return ("#FF0700FF");
                    }
                    else if (d.group == 110) {
                        return ("#FF9F00FF");
                    }
                    else if (d.group == 101) {
                        return ("#FF6000FF");
                    }
                    else if (d.group == 93) {
                        return ("#FF2200FF");
                    }
                    else if (d.group == 53) {
                        return ("#FF1200FF");
                    }
                    else if (d.group == 108) {
                        return ("#FF9100FF");
                    }
                    else if (d.group == 69) {
                        return ("#FFA400FF");
                    }
                    else if (d.group == 75) {
                        return ("#FFDB00FF");
                    }
                    else if (d.group == 76) {
                        return ("#FFE400FF");
                    }
                    else if (d.group == 119) {
                        return ("#FFE300FF");
                    }
                    else if (d.group == 134) {
                        return ("#FFFFF4FF");
                    }
                    else if (d.group == 62) {
                        return ("#FF6400FF");
                    }
                    else if (d.group == 127) {
                        return ("#FFFF60FF");
                    }
                    else if (d.group == 121) {
                        return ("#FFF100FF");
                    }
                    else if (d.group == 109) {
                        return ("#FF9800FF");
                    }
                    else if (d.group == 116) {
                        return ("#FFCF00FF");
                    }
                    else if (d.group == 124) {
                        return ("#FFFF20FF");
                    }
                    else if (d.group == 131) {
                        return ("#FFFFB5FF");
                    }
                    else if (d.group == 90) {
                        return ("#FF0E00FF");
                    }
                    else if (d.group == 114) {
                        return ("#FFBA00FF");
                    }
                    else if (d.group == 72) {
                        return ("#FFBF00FF");
                    }
                    else if (d.group == 52) {
                        return ("#FF0900FF");
                    }
                    else if (d.group == 63) {
                        return ("#FF6D00FF");
                    }
                    else if (d.group == 79) {
                        return ("#FFFF00FF");
                    }
                    else if (d.group == 80) {
                        return ("#FFFF0EFF");
                    }
                    else if (d.group == 78) {
                        return ("#FFF600FF");
                    }
                    else if (d.group == 107) {
                        return ("#FF8A00FF");
                    }
                    else if (d.group == 87) {
                        return ("#FFFFD4FF");
                    }
                    else if (d.group == 59) {
                        return ("#FF4900FF");
                    }
                    else if (d.group == 55) {
                        return ("#FF2400FF");
                    }
                    else if (d.group == 106) {
                        return ("#FF8300FF");
                    }
                    else if (d.group == 113) {
                        return ("#FFB300FF");
                    }
                    else if (d.group == 51) {
                        return ("#FF0000FF");
                    }
                    else if (d.group == 74) {
                        return ("#FFD100FF");
                    }
                    else if (d.group == 82) {
                        return ("#FFFF47FF");
                    }
                    else if (d.group == 104) {
                        return ("#FF7500FF");
                    }
                    else if (d.group == 66) {
                        return ("#FF8900FF");
                    }
                    else if (d.group == 133) {
                        return ("#FFFFDFFF");
                    }
                    else if (d.group == 86) {
                        return ("#FFFFB8FF");
                    }
                    else if (d.group == 65) {
                        return ("#FF8000FF");
                    }
                    else if (d.group == 132) {
                        return ("#FFFFCAFF");
                    }
                    else if (d.group == 58) {
                        return ("#FF4000FF");
                    }
                    else if (d.group == 105) {
                        return ("#FF7C00FF");
                    }
                    else if (d.group == 102) {
                        return ("#FF6700FF");
                    }
                    else if (d.group == 96) {
                        return ("#FF3E00FF");
                    }
                    else if (d.group == 125) {
                        return ("#FFFF35FF");
                    }
                    else if (d.group == 81) {
                        return ("#FFFF2BFF");
                    }
                    else if (d.group == 83) {
                        return ("#FFFF63FF");
                    }
                    else if (d.group == 120) {
                        return ("#FFEA00FF");
                    }
                    else if (d.group == 71) {
                        return ("#FFB600FF");
                    }
                    else if (d.group == 67) {
                        return ("#FF9200FF");
                    }
                    else if (d.group == 97) {
                        return ("#FF4500FF");
                    }
                    else if (d.group == 112) {
                        return ("#FFAC00FF");
                    }
                    else if (d.group == 61) {
                        return ("#FF5B00FF");
                    }
                    else if (d.group == 91) {
                        return ("#FF1500FF");
                    }
                    else if (d.group == 115) {
                        return ("#FFC100FF");
                    }
                    else if (d.group == 103) {
                        return ("#FF6E00FF");
                    }
                    else if (d.group == 70) {
                        return ("#FFAD00FF");
                    }
                    else if (d.group == 84) {
                        return ("#FFFF80FF");
                    }
                    else if (d.group == 126) {
                        return ("#FFFF4AFF");
                    }
                    else if (d.group == 100) {
                        return ("#FF5A00FF");
                    }
                    else if (d.group == 77) {
                        return ("#FFED00FF");
                    }
                    else if (d.group == 68) {
                        return ("#FF9B00FF");
                    }
                    else if (d.group == 57) {
                        return ("#FF3700FF");
                    }
                    else if (d.group == 92) {
                        return ("#FF1C00FF");
                    }
                    else if (d.group == 60) {
                        return ("#FF5200FF");
                    }
                    else if (d.group == 111) {
                        return ("#FFA500FF");
                    }
                    else if (d.group == 94) {
                        return ("#FF2900FF");
                    }
                    else if (d.group == 128) {
                            return ("#FFFF75FF");
                        }

                        else {
                            return ("#000000");
                        }


                    // if (d.group == 0) {
                    //     return colorScale(d.value);
                    // }
                    // else {
                    //
                    //     if (d.group == 1) {
                    //         return("#ed0909");
                    //     }
                    //     if (d.group == 2) {
                    //         return("#0af702");
                    //     }
                    //     if (d.group == 3) {
                    //         return("#FF00FF");
                    //     }
                    //     if (d.group == 4) {
                    //         return("#808000");
                    //     }
                    //     if (d.group == 5) {
                    //         return("#000080");
                    //     }
                    //     if (d.group == 6) {
                    //         return("#800080");
                    //     }
                    //     if (d.group == 7) {
                    //         return("#00ffff");
                    //     }
                    //     if (d.group == 8) {
                    //         return("#F5F5DC");
                    //     }
                    //     if (d.group == 9) {
                    //         return("#A52A2A");
                    //     }
                    //     if (d.group == 10) {
                    //         return("#8B0000");
                    //     }
                    //     if (d.group == 11) {
                    //         return("#FF8C00");
                    //     }
                    //
                    // }

                })

                // .style("fill", function (d) {
                //     return colNodeScale(d.group);
                // })
                .style("stroke", "#333")
                .style("stroke-width", "2px")
                .style("stroke-dasharray",
                    function (d) {
                        if (d.connected == "No") {
                            ////console.log("not connected");
                            return (5, 5);

                        }
                        else if (d.connected == "Yes") {
                            ////console.log("connected");
                            return (3, 0);
                        }
                    })

                //.attr("class", "node")
                .on("mouseenter", function (d) {
                    is_connected(d, 0.1)
                    node.transition().duration(100).attr("r", function (d) {
                        return xScale(d.weight);
                    })
                    d3.select(this).transition().duration(100).attr("r", function (d) {
                        return xScale(d.weight + 3);
                    })
                })
                .on("mouseleave", function (d) {
                    node.transition().duration(100).attr("r", function (d) {
                        return xScale(d.weight);
                    })
                    //is_connected(d, 1);
                })
                .on("click", function (d) {

                    //if(!first_click) {
                    is_connected_on_click(d, 0.1);
                    node.transition().duration(100).attr("r", function (d) {
                        return xScale(d.weight);
                    })
                    d3.select(this).transition().duration(100).attr("r", function (d) {
                        return xScale(d.weight + 3);
                    })

                })
                .call(force.drag);

            var labels = gnodes.append("text")
                .attr("dx", 4)
                .attr("dy", 4)
                .style("font", String(fontSize) + "px Arial")
                .attr("text-anchor", function (d) {
                    return d.x < w / 2 ? "end" : "start";
                })
                .attr("transform", function (d) {
                    return d.x < w / 2 ? "rotate(" + Math.atan((d.y - w / 2) / (d.x - w / 2)) * 180 / Math.PI + ")translate(-20)" : "rotate(" + Math.atan((d.y - w / 2) / (d.x - w / 2)) * 180 / Math.PI + ")translate(20)";
                })
                //.attr("transform", function(d) { return  "rotate(" +Math.atan((d.y-w/2)/(d.x-w/2))*180/Math.PI+ ")"})
                //.attr("transform", function(d) { return (d.x-w/2)/(d.y-w/2) < 0 ?  "rotate(" +Math.atan((d.y-w/2)/(d.x-w/2))*180/Math.PI+ ")" : "rotate(180)"; })
                .text(function (d) {
                    return d.full_name
                })

            var drag = force.drag()
                .on("dragstart", dragstart);
            //.on("dragstart", dragstartAll);


            //For not moving after drag
            function dragstart(d) {
                d3.select(this).classed("fixed", d.fixed = true);

                for (i = 0; i < nodes.length; i++) {
                    nodes[i].fixed = true;
                }
            }


            var svgText = svgGE.append("text");
            svgText.attr("x", 10).attr("y", globalHPlus50 - 50).text("PiNET-server @ www.pinet-server.org").style("font", "14px Times New Roman");

            //Added from here for coloring the legend
            max_data = 1000;
            min_data = -1000;
            if (1 == 0) {

                var colors = ["#00A6FF", "#1097E0", "#2885B7", "#35799E", "#4C7991", "#6D828D", "#8C8C8C", "#8E8E5C", "#92923C", "#A5A52E", "#BDBD24", "#DDDD15", "#FFFF00"];
                var domain_data = [-2.0, -1.6, -1.2, -0.8, -0.4, -0.01, 0.01, 0.4, 0.8, 1.2, 1.6, 2.0, 1000];


                var colorScale2 = d3.scale.threshold()
                    .domain(domain_data)
                    .range(colors);


                var legend2 = svgGE.selectAll(".legend")

                //.data([min_data, min_data + (max_data - min_data) / 7, min_data + 2 * (max_data - min_data) / 7, min_data + 3 * (max_data - min_data) / 7, min_data + 4 * (max_data - min_data) / 7, min_data + 5 * (max_data - min_data) / 7, min_data + 6 * (max_data - min_data) / 7], function (d) {
                    .data([-2.0, -1.6, -1.2, -0.8, -0.4, -0.01, 0.01, 0.4, 0.8, 1.2, 1.6, 2.0, 10.0], function (d) {

                        return d;
                    });

                // //console.log("colorScale.quantiles()");
                // //console.log(colorScale.quantiles());
                legend2.enter().append("g")
                    .attr("class", "legend");
                var gridSize = Math.floor(globalW / 40);
                var legendElementWidth = gridSize * 2;
                legend2.append("rect")
                    .attr("x", function (d, i) {
                        return legendElementWidth * i;
                    })
                    .attr("y", globalHPlus50 - 40)
                    .attr("width", legendElementWidth)
                    .attr("height", gridSize / 2)
                    .style("fill", function (d, i) {
                        return colors[i];
                    });

                legend2.append("text")
                //.attr("class", "mono")
                    .text(function (d, i) {
                        if (i == 0) {
                            return " a < " + parseFloat(Math.round(d * 100) / 100).toFixed(1);
                        }
                        else if (i == svgGE.selectAll(".legend").data().length - 1) {

                            return parseFloat(Math.round((svgGE.selectAll(".legend").data()[i - 1]) * 100) / 100).toFixed(1) + " ≤ a ";
                        }
                        else {

                            return parseFloat(Math.round((svgGE.selectAll(".legend").data()[i - 1]) * 100) / 100).toFixed(1) + " ≤ a < " + parseFloat(Math.round(d * 100) / 100).toFixed(1);
                        }
                        //return  parseFloat(Math.round(d * 100) / 100).toFixed(2) + "≥ a";
                    })
                    .style("font", "11px Times New Roman")
                    .attr("x", function (d, i) {
                        return legendElementWidth * i;
                    })
                    .attr("y", globalHPlus50 - 40 + gridSize);

                legend2.exit().remove();
            }


        };
        d3.select('#circularViewGE').on('click', function () {
            circularViewGE();
            self.graphType = 1;
        });

        function circosViewGE() {
            svgGE.remove();

            xScale.domain(d3.extent(nodes, function (d) {
                return d.weight;
            }));
            scoreScale.domain(d3.extent(links, function (d) {
                return d.weight;
            }));
            colNodeScale.domain(d3.extent(nodes, function (d) {
                return d.group;
            }));
            colScale.domain(d3.extent(links, function (d) {
                return d.weight;
            }));
            var margin = 75,
                w = widthSize - 2 * margin,
                h = w,
                radius = w / 2,
                strokeWidth = 4,
                hyp2 = Math.pow(radius, 2),
                nodeBaseRad = 5;


            globalH = h;
            globalHPlus50 = h + 50;
            globalW = w;

            var first_click = false;


            svgGE = d3.select("#chartGE")
                .append("svg")
                .attr("style", "outline: thin solid yellow;")
                .attr("width", w)
                .attr("height", globalHPlus50);
            svgGE.append("rect")
                .attr("width", "100%")
                .attr("height", "100%")
                .attr("fill", "white");


            // This is for grouping nodes


            var force = d3.layout.force()
                .nodes(nodes)
                .links(links)
                .size([w, h]);

// evenly spaces nodes along arc
            var circleCoord = function (node, index, input_num_nodes, has_focus) {
                //console.log("in circleCoord");

                // console.log(node["name"]);
                // console.log(index);
                // String(node["name"]).valueOf() ==
                var circumference = circle.node().getTotalLength();
                var pointAtLength = function (l) {
                    return circle.node().getPointAtLength(l)
                };


                if (has_focus) {
                    var added_num = parseInt(input_num_nodes / 4);
                    if (added_num % 2 == 1) {
                        added_num += 1;
                    }
                    var num_nodes = input_num_nodes + added_num;
                    var sectionLength = (circumference) / num_nodes;
                    if (String(node["name"]).valueOf() === self.interest) {
                        var position = 0;
                        // console.log("in ATP");
                        // console.log(pointAtLength(circumference - position));
                        // console.log(position);
                    }
                    else {


                        var position = sectionLength * (index + added_num / 2) + sectionLength / 2;
                    }
                }
                else {
                    var num_nodes = input_num_nodes;
                    var sectionLength = (circumference) / num_nodes;
                    var position = sectionLength * (index) + sectionLength / 2;

                }

                //console.log(pointAtLength(circumference - position));
                return pointAtLength(circumference - position)
            }

            var is_connected = function (d, opacity) {
                lines.transition().style("stroke-opacity", function (o) {
                    return o.source === d || o.target === d ? 1 : opacity;
                });
            }


            // lines.transition().style("stroke-opacity", function (o) {
            //     if (o.source === d || o.target === d){
            //         return 1;
            //     }
            //
            // });

            var is_connected_on_click = function (d, opacity) {
                //console.log(d);
                lines.transition().style("stroke-opacity", function (o) {
                    return o.source.group === d.group || o.target.group === d.group ? 1 : opacity;
                });
            }

            // var dim = w - 400
            // var circle = svgGE.append("path")
            //     .attr("d", "M 200, " + (dim / 2 + 200) + " a " + dim / 2 + "," + dim / 2 + " 0 1,0 " + dim + ",0 a " + dim / 2 + "," + dim / 2 + " 0 1,0 " + dim * -1 + ",0")
            //     .style("fill", "white");

            var dim = w - (widthSize - circleSize)
            var circle = svgGE.append("path")
                .attr("d", "M " + String((widthSize - circleSize) / 2) + ", " + (dim / 2 + (widthSize - circleSize) / 2) + " a " + dim / 2 + "," + dim / 2 + " 0 1,0 " + dim + ",0 a " + dim / 2 + "," + dim / 2 + " 0 1,0 " + dim * -1 + ",0")
                .style("fill", "white");

            force.start();
            var has_focus = false;
            nodes.forEach(function (n, i) {
                if (String(n["name"]).valueOf() == self.interest) {
                    //if (String(n["name"]).valueOf() === $scope.interest) {
                    has_focus = true;
                }

            })

            console.log(has_focus);
            nodes.forEach(function (n, i) {
                var coord = circleCoord(n, i, nodes.length, has_focus)
                // console.log("calculating coor");
                // console.log(coord);
                // console.log(coord.x);
                // console.log(coord.y);
                n.x = coord.x
                n.y = coord.y
            });


            // use this one for straight line links...
            // var lines = svg.selectAll("line.node-link")
            //     .data(links).enter().append("line")
            //     .attr("class", "node-link")
            //     .attr("x1", function(d) { return d.source.x; })
            //     .attr("y1", function(d) { return d.source.y; })
            //     .attr("x2", function(d) { return d.target.x; })
            //     .attr("y2", function(d) { return d.target.y; });

            var lines = svgGE.selectAll("path.node-link")
                .data(links).enter().append("path")
                .style("fill", "none")
                .style("stroke", function (d) {


                    if (d.tag == 0) {
                        return ("#696969");
                    }

                    else if (d.tag == 1) {
                        return ("#006400");
                    }
                    else if (d.tag == 2) {
                        return ("#00FF00");
                    }
                    else if (d.tag == 3) {
                        return ("#0000FF");
                    }
                    else if (d.tag == 4) {
                        return ("#808080");
                    }
                    else if (d.tag == 5) {
                        return ("#8B4513");
                    }
                    else if (d.tag == 6) {
                        return ("#FFFFE0");
                    }
                    else if (d.tag == 7) {
                        return ("#8464c5");
                    }
                    else if (d.tag == 8) {
                        return ("#00FFFF");
                    }
                    else if (d.tag == 9) {
                        return ("#FF7F50");
                    }
                    else if (d.tag == 10) {
                        return ("#FF0000");
                    }
                    else if (d.tag == 11) {
                        return ("#FF00FF");
                    }
                    else if (d.tag == 12) {
                        return ("#8FBC8F");
                    }
                    else if (d.tag == 13) {
                        return ("#A52A2A");
                    }
                    else if (d.tag == 14) {
                        return ("#FFD700");
                    }
                    else if (d.tag == 15) {
                        return ("#A0522D");
                    }
                    else if (d.tag == 16) {
                        return ("#FFFF00");
                    }
                    else if (d.tag == 17) {
                        return ("#6A5ACD");
                    }
                    else if (d.tag == 18) {
                        return ("#708090");
                    }
                    else if (d.tag == 19) {
                        return ("#FF6347");
                    }
                    else if (d.tag == 20) {
                        return ("#CD5C5C");
                    }
                    else if (d.tag == 21) {
                        return ("#DB7093");
                    }
                    else if (d.tag == 22) {
                        return ("#2E8B57");
                    }
                    else if (d.tag == 23) {
                        return ("#000080");
                    }
                    else if (d.tag == 24) {
                        return ("#9370DB");
                    }
                    else if (d.tag == 25) {
                        return ("#A52A2A");
                    }
                    else if (d.tag == 26) {
                        return ("#FDF5E6");
                    }
                    else if (d.tag == 27) {
                        return ("#7B68EE");
                    }
                    else if (d.tag == 28) {
                        return ("#696969");
                    }
                    else if (d.tag == 29) {
                        return ("#FF4500");
                    }
                    else if (d.tag == 30) {
                        return ("#DC143C");
                    }
                    else if (d.tag == 31) {
                        return ("#FF69B4");
                    }
                    else if (d.tag == 32) {
                        return ("#006400");
                    }
                    else if (d.tag == 33) {
                        return ("#87CEEB");
                    }
                    else if (d.tag == 34) {
                        return ("#EE82EE");
                    }
                    else if (d.tag == 35) {
                        return ("#800000");
                    }
                    else if (d.tag == 36) {
                        return ("#FAEBD7");
                    }
                    else if (d.tag == 37) {
                        return ("#4B0082");
                    }
                    else if (d.tag == 38) {
                        return ("#808080");
                    }
                    else if (d.tag == 39) {
                        return ("#FF8C00");
                    }
                    else if (d.tag == 40) {
                        return ("#FA8072");
                    }
                    else if (d.tag == 41) {
                        return ("#FFC0CB");
                    }
                    else if (d.tag == 42) {
                        return ("#9ACD32");
                    }
                    else if (d.tag == 43) {
                        return ("#4682B4");
                    }
                    else if (d.tag == 44) {
                        return ("#DDA0DD");
                    }
                    else if (d.tag == 45) {
                        return ("#CD853F");
                    }
                    else if (d.tag == 46) {
                        return ("#FFE4E1");
                    }
                    else if (d.tag == 47) {
                        return ("#696969");
                    }
                    else if (d.tag == 48) {
                        return ("#A9A9A9");
                    }
                    else if (d.tag == 49) {
                        return ("#FFA500");
                    }
                    else {
                        return ("#000000");
                    }


                    // if (d.group == 0) {
                    //     return colorScale(d.value);
                    // }
                    // else {
                    //
                    //     if (d.group == 1) {
                    //         return("#ed0909");
                    //     }
                    //     if (d.group == 2) {
                    //         return("#0af702");
                    //     }
                    //     if (d.group == 3) {
                    //         return("#FF00FF");
                    //     }
                    //     if (d.group == 4) {
                    //         return("#808000");
                    //     }
                    //     if (d.group == 5) {
                    //         return("#000080");
                    //     }
                    //     if (d.group == 6) {
                    //         return("#800080");
                    //     }
                    //     if (d.group == 7) {
                    //         return("#00ffff");
                    //     }
                    //     if (d.group == 8) {
                    //         return("#F5F5DC");
                    //     }
                    //     if (d.group == 9) {
                    //         return("#A52A2A");
                    //     }
                    //     if (d.group == 10) {
                    //         return("#8B0000");
                    //     }
                    //     if (d.group == 11) {
                    //         return("#FF8C00");
                    //     }
                    //
                    // }

                })



                //.style("stroke", "#726363")
                .attr("class", "node-link")
                .style("stroke-width", function (d) {
                    return scoreScale(d.weight);
                })
                //.style("stroke-width", 0.1)
                .attr("d", function (d) {

                    var dx = d.target.x - d.source.x,
                        dy = d.target.y - d.source.y,
                        dr = Math.sqrt(dx * dx + dy * dy),
                        a1 = dx,
                        a2 = dy,
                        c1 = w / 2 - d.source.x,
                        c2 = h / 2 - d.source.y,
                        d1 = w / 2 - d.target.x,
                        d2 = h / 2 - d.target.y,

                        drx = dr / 1.5,
                        dry = dr / 1.5,
                        xRotation = 0, // degrees
                        largeArc = 0, // 1 or 0

                        sweep = 1, // 1 or 0
                        x2 = d.target.x,
                        y2 = d.target.y;


                    // if( (a1*c2 - a2*c1) > 0)
                    // {
                    //     sweep = 0
                    // }
                    // else
                    // {sweep = 1}
                    if ((c1 * d2 - c2 * d1) > 0) {
                        sweep = 0
                    }
                    else {
                        sweep = 1
                    }


                    return "M" + d.source.x + "," + d.source.y + "A" + drx + "," + dry + " " + xRotation + "," + largeArc + "," + sweep + " " + x2 + "," + y2;


                    //return "M" + d.source.x + "," + d.source.y + ","+ d.target.x + "," + d.target.y;
                    //return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
                });


            //     var dx = d.target.x - d.source.x,
            //         dy = d.target.y - d.source.y,
            //         dr = Math.sqrt(dx * dx + dy * dy);
            //     return "M" +
            //         d.source.x + "," +
            //         d.source.y + "," +
            //         d.target.x + "," +
            //         d.target.y;
            //
            // });


            var gnodes = svgGE.selectAll('g.gnode')
                .data(nodes).enter().append('g')
                .attr("transform", function (d) {
                    return "translate(" + d.x + "," + d.y + ")"
                })
                .classed('gnode', true);


            // node.append("circle")
            //     .attr("r", function (d) { return xScale(d.weight); })
            //     .style("fill", function(d) { return colNodeScale(d.group); });

//                 function click() {
//                     d3.select(this).select("text").transition()
//                         .duration(750)
//                         .attr("x", 22)
//                         .style("stroke", "lightsteelblue")
//                         .style("stroke-width", ".5px")
//                         .style("font", "20px sans-serif");
//                     d3.select(this).select("circle").transition()
//                         .duration(750)
//                         .attr("r", 16);
//                 }
//
// // action to take on mouse double click
//                 function dblclick() {
//                     d3.select(this).select("circle").transition()
//                         .duration(750)
//                         .attr("r", 6);
//                     d3.select(this).select("text").transition()
//                         .duration(750)
//                         .attr("x", 12)
//                         .style("stroke", "none")
//                         .style("fill", "black")
//                         .style("stroke", "none")
//                         .style("font", "10px sans-serif");
//                 }


            var node = gnodes.append("circle")
                .attr("r", function (d) {
                    return xScale(d.weight);
                })
                .style("fill", function (d) {


                    if (d.group == 0) {
                        return ("#696969");
                    }
                    else if (d.group == 1) {
                        return ("#006400");
                    }
                    else if (d.group == 2) {
                        return ("#00FF00");
                    }
                    else if (d.group == 3) {
                        return ("#0000FF");
                    }
                    else if (d.group == 4) {
                        return ("#808080");
                    }
                    else if (d.group == 5) {
                        return ("#8B4513");
                    }
                    else if (d.group == 6) {
                        return ("#FFFFE0");
                    }
                    else if (d.group == 7) {
                        return ("#8464c5");
                    }
                    else if (d.group == 8) {
                        return ("#00FFFF");
                    }
                    else if (d.group == 9) {
                        return ("#FF7F50");
                    }
                    else if (d.group == 10) {
                        return ("#FF0000");
                    }
                    else if (d.group == 11) {
                        return ("#FF00FF");
                    }
                    else if (d.group == 12) {
                        return ("#8FBC8F");
                    }
                    else if (d.group == 13) {
                        return ("#A52A2A");
                    }
                    else if (d.group == 14) {
                        return ("#FFD700");
                    }
                    else if (d.group == 15) {
                        return ("#A0522D");
                    }
                    else if (d.group == 16) {
                        return ("#FFFF00");
                    }
                    else if (d.group == 17) {
                        return ("#6A5ACD");
                    }
                    else if (d.group == 18) {
                        return ("#708090");
                    }
                    else if (d.group == 19) {
                        return ("#FF6347");
                    }
                    else if (d.group == 20) {
                        return ("#CD5C5C");
                    }
                    else if (d.group == 21) {
                        return ("#DB7093");
                    }
                    else if (d.group == 22) {
                        return ("#2E8B57");
                    }
                    else if (d.group == 23) {
                        return ("#000080");
                    }
                    else if (d.group == 24) {
                        return ("#9370DB");
                    }
                    else if (d.group == 25) {
                        return ("#A52A2A");
                    }
                    else if (d.group == 26) {
                        return ("#FDF5E6");
                    }
                    else if (d.group == 27) {
                        return ("#7B68EE");
                    }
                    else if (d.group == 28) {
                        return ("#696969");
                    }
                    else if (d.group == 29) {
                        return ("#FF4500");
                    }
                    else if (d.group == 30) {
                        return ("#DC143C");
                    }
                    else if (d.group == 31) {
                        return ("#FF69B4");
                    }
                    else if (d.group == 32) {
                        return ("#006400");
                    }
                    else if (d.group == 33) {
                        return ("#87CEEB");
                    }
                    else if (d.group == 34) {
                        return ("#EE82EE");
                    }
                    else if (d.group == 35) {
                        return ("#800000");
                    }
                    else if (d.group == 36) {
                        return ("#FAEBD7");
                    }
                    else if (d.group == 37) {
                        return ("#4B0082");
                    }
                    else if (d.group == 38) {
                        return ("#808080");
                    }
                    else if (d.group == 39) {
                        return ("#FF8C00");
                    }
                    else if (d.group == 40) {
                        return ("#FA8072");
                    }
                    else if (d.group == 41) {
                        return ("#FFC0CB");
                    }
                    else if (d.group == 42) {
                        return ("#9ACD32");
                    }
                    else if (d.group == 43) {
                        return ("#4682B4");
                    }
                    else if (d.group == 44) {
                        return ("#DDA0DD");
                    }
                    else if (d.group == 45) {
                        return ("#CD853F");
                    }
                    else if (d.group == 46) {
                        return ("#FFE4E1");
                    }
                    else if (d.group == 47) {
                        return ("#696969");
                    }
                    else if (d.group == 48) {
                        return ("#A9A9A9");
                    }
                    else if (d.group == 49) {
                        return ("#FFA500");
                    }
                    else if (d.group == 117) {
                        return ("#FFD600FF");
                    }
                    else if (d.group == 64) {
                        return ("#FF7600FF");
                    }
                    else if (d.group == 85) {
                        return ("#FFFF9CFF");
                    }
                    else if (d.group == 95) {
                        return ("#FF3000FF");
                    }
                    else if (d.group == 123) {
                        return ("#FFFF0BFF");
                    }
                    else if (d.group == 88) {
                        return ("#FFFFF1FF");
                    }
                    else if (d.group == 73) {
                        return ("#FFC800FF");
                    }
                    else if (d.group == 118) {
                        return ("#FFDD00FF");
                    }
                    else if (d.group == 129) {
                        return ("#FFFF8AFF");
                    }
                    else if (d.group == 54) {
                        return ("#FF1B00FF");
                    }
                    else if (d.group == 122) {
                        return ("#FFF800FF");
                    }
                    else if (d.group == 130) {
                        return ("#FFFF9FFF");
                    }
                    else if (d.group == 99) {
                        return ("#FF5300FF");
                    }
                    else if (d.group == 98) {
                        return ("#FF4C00FF");
                    }
                    else if (d.group == 56) {
                        return ("#FF2E00FF");
                    }
                    else if (d.group == 89) {
                        return ("#FF0700FF");
                    }
                    else if (d.group == 110) {
                        return ("#FF9F00FF");
                    }
                    else if (d.group == 101) {
                        return ("#FF6000FF");
                    }
                    else if (d.group == 93) {
                        return ("#FF2200FF");
                    }
                    else if (d.group == 53) {
                        return ("#FF1200FF");
                    }
                    else if (d.group == 108) {
                        return ("#FF9100FF");
                    }
                    else if (d.group == 69) {
                        return ("#FFA400FF");
                    }
                    else if (d.group == 75) {
                        return ("#FFDB00FF");
                    }
                    else if (d.group == 76) {
                        return ("#FFE400FF");
                    }
                    else if (d.group == 119) {
                        return ("#FFE300FF");
                    }
                    else if (d.group == 134) {
                        return ("#FFFFF4FF");
                    }
                    else if (d.group == 62) {
                        return ("#FF6400FF");
                    }
                    else if (d.group == 127) {
                        return ("#FFFF60FF");
                    }
                    else if (d.group == 121) {
                        return ("#FFF100FF");
                    }
                    else if (d.group == 109) {
                        return ("#FF9800FF");
                    }
                    else if (d.group == 116) {
                        return ("#FFCF00FF");
                    }
                    else if (d.group == 124) {
                        return ("#FFFF20FF");
                    }
                    else if (d.group == 131) {
                        return ("#FFFFB5FF");
                    }
                    else if (d.group == 90) {
                        return ("#FF0E00FF");
                    }
                    else if (d.group == 114) {
                        return ("#FFBA00FF");
                    }
                    else if (d.group == 72) {
                        return ("#FFBF00FF");
                    }
                    else if (d.group == 52) {
                        return ("#FF0900FF");
                    }
                    else if (d.group == 63) {
                        return ("#FF6D00FF");
                    }
                    else if (d.group == 79) {
                        return ("#FFFF00FF");
                    }
                    else if (d.group == 80) {
                        return ("#FFFF0EFF");
                    }
                    else if (d.group == 78) {
                        return ("#FFF600FF");
                    }
                    else if (d.group == 107) {
                        return ("#FF8A00FF");
                    }
                    else if (d.group == 87) {
                        return ("#FFFFD4FF");
                    }
                    else if (d.group == 59) {
                        return ("#FF4900FF");
                    }
                    else if (d.group == 55) {
                        return ("#FF2400FF");
                    }
                    else if (d.group == 106) {
                        return ("#FF8300FF");
                    }
                    else if (d.group == 113) {
                        return ("#FFB300FF");
                    }
                    else if (d.group == 51) {
                        return ("#FF0000FF");
                    }
                    else if (d.group == 74) {
                        return ("#FFD100FF");
                    }
                    else if (d.group == 82) {
                        return ("#FFFF47FF");
                    }
                    else if (d.group == 104) {
                        return ("#FF7500FF");
                    }
                    else if (d.group == 66) {
                        return ("#FF8900FF");
                    }
                    else if (d.group == 133) {
                        return ("#FFFFDFFF");
                    }
                    else if (d.group == 86) {
                        return ("#FFFFB8FF");
                    }
                    else if (d.group == 65) {
                        return ("#FF8000FF");
                    }
                    else if (d.group == 132) {
                        return ("#FFFFCAFF");
                    }
                    else if (d.group == 58) {
                        return ("#FF4000FF");
                    }
                    else if (d.group == 105) {
                        return ("#FF7C00FF");
                    }
                    else if (d.group == 102) {
                        return ("#FF6700FF");
                    }
                    else if (d.group == 96) {
                        return ("#FF3E00FF");
                    }
                    else if (d.group == 125) {
                        return ("#FFFF35FF");
                    }
                    else if (d.group == 81) {
                        return ("#FFFF2BFF");
                    }
                    else if (d.group == 83) {
                        return ("#FFFF63FF");
                    }
                    else if (d.group == 120) {
                        return ("#FFEA00FF");
                    }
                    else if (d.group == 71) {
                        return ("#FFB600FF");
                    }
                    else if (d.group == 67) {
                        return ("#FF9200FF");
                    }
                    else if (d.group == 97) {
                        return ("#FF4500FF");
                    }
                    else if (d.group == 112) {
                        return ("#FFAC00FF");
                    }
                    else if (d.group == 61) {
                        return ("#FF5B00FF");
                    }
                    else if (d.group == 91) {
                        return ("#FF1500FF");
                    }
                    else if (d.group == 115) {
                        return ("#FFC100FF");
                    }
                    else if (d.group == 103) {
                        return ("#FF6E00FF");
                    }
                    else if (d.group == 70) {
                        return ("#FFAD00FF");
                    }
                    else if (d.group == 84) {
                        return ("#FFFF80FF");
                    }
                    else if (d.group == 126) {
                        return ("#FFFF4AFF");
                    }
                    else if (d.group == 100) {
                        return ("#FF5A00FF");
                    }
                    else if (d.group == 77) {
                        return ("#FFED00FF");
                    }
                    else if (d.group == 68) {
                        return ("#FF9B00FF");
                    }
                    else if (d.group == 57) {
                        return ("#FF3700FF");
                    }
                    else if (d.group == 92) {
                        return ("#FF1C00FF");
                    }
                    else if (d.group == 60) {
                        return ("#FF5200FF");
                    }
                    else if (d.group == 111) {
                        return ("#FFA500FF");
                    }
                    else if (d.group == 94) {
                        return ("#FF2900FF");
                    }
                    else if (d.group == 128) {
                            return ("#FFFF75FF");
                        }

                        else {
                            return ("#000000");
                        }


                    // if (d.group == 0) {
                    //     return colorScale(d.value);
                    // }
                    // else {
                    //
                    //     if (d.group == 1) {
                    //         return("#ed0909");
                    //     }
                    //     if (d.group == 2) {
                    //         return("#0af702");
                    //     }
                    //     if (d.group == 3) {
                    //         return("#FF00FF");
                    //     }
                    //     if (d.group == 4) {
                    //         return("#808000");
                    //     }
                    //     if (d.group == 5) {
                    //         return("#000080");
                    //     }
                    //     if (d.group == 6) {
                    //         return("#800080");
                    //     }
                    //     if (d.group == 7) {
                    //         return("#00ffff");
                    //     }
                    //     if (d.group == 8) {
                    //         return("#F5F5DC");
                    //     }
                    //     if (d.group == 9) {
                    //         return("#A52A2A");
                    //     }
                    //     if (d.group == 10) {
                    //         return("#8B0000");
                    //     }
                    //     if (d.group == 11) {
                    //         return("#FF8C00");
                    //     }
                    //
                    // }

                })
                // .style("fill", function (d) {
                //     return colNodeScale(d.group);
                // })
                .style("stroke", "#333")
                .style("stroke-width", "2px")
                .style("stroke-dasharray",
                    function (d) {
                        if (d.connected == "No") {
                            ////console.log("not connected");
                            return (5, 5);

                        }
                        else if (d.connected == "Yes") {
                            ////console.log("connected");
                            return (3, 0);
                        }
                    })

                //.attr("class", "node")
                .on("mouseenter", function (d) {
                    is_connected(d, 0.1)
                    node.transition().duration(100).attr("r", function (d) {
                        return xScale(d.weight);
                    })
                    d3.select(this).transition().duration(100).attr("r", function (d) {
                        return xScale(d.weight + 3);
                    })
                })
                // .on("mouseleave", function (d) {
                //     node.transition().duration(100).attr("r", function (d) {
                //         return xScale(d.weight);
                //     })
                //     //is_connected(d, 1);
                // })
                .on("click", function (d) {

                    //if(!first_click) {
                    is_connected_on_click(d, 0.1);
                    node.transition().duration(100).attr("r", function (d) {
                        return xScale(d.weight);
                    })
                    d3.select(this).transition().duration(100).attr("r", function (d) {
                        return xScale(d.weight + 3);
                    })

                })

                .call(force.drag);

            var labels = gnodes.append("text")
                .attr("dx", 4)
                .attr("dy", 4)
                .style("font", String(fontSize) + "px Arial")
                .attr("text-anchor", function (d) {
                    return d.x < w / 2 ? "end" : "start";
                })
                .attr("transform", function (d) {
                    return d.x < w / 2 ? "rotate(" + Math.atan((d.y - w / 2) / (d.x - w / 2)) * 180 / Math.PI + ")translate(-20)" : "rotate(" + Math.atan((d.y - w / 2) / (d.x - w / 2)) * 180 / Math.PI + ")translate(20)";
                })
                //.attr("transform", function(d) { return  "rotate(" +Math.atan((d.y-w/2)/(d.x-w/2))*180/Math.PI+ ")"})
                //.attr("transform", function(d) { return (d.x-w/2)/(d.y-w/2) < 0 ?  "rotate(" +Math.atan((d.y-w/2)/(d.x-w/2))*180/Math.PI+ ")" : "rotate(180)"; })
                .text(function (d) {
                    return d.full_name
                })

            var drag = force.drag()
                .on("dragstart", dragstart);
            //.on("dragstart", dragstartAll);


            //For not moving after drag
            function dragstart(d) {
                d3.select(this).classed("fixed", d.fixed = true);

                for (i = 0; i < nodes.length; i++) {
                    nodes[i].fixed = true;
                }
            }


            var svgText = svgGE.append("text");
            svgText.attr("x", 10).attr("y", globalHPlus50 - 50).text("PiNET-server @ www.pinet-server.org").style("font", "14px Times New Roman");

            //Added from here for coloring the legend
            max_data = 1000;
            min_data = -1000;

            if (1 == 0) {
                var colors = ["#00A6FF", "#1097E0", "#2885B7", "#35799E", "#4C7991", "#6D828D", "#8C8C8C", "#8E8E5C", "#92923C", "#A5A52E", "#BDBD24", "#DDDD15", "#FFFF00"];
                var domain_data = [-2.0, -1.6, -1.2, -0.8, -0.4, -0.01, 0.01, 0.4, 0.8, 1.2, 1.6, 2.0, 1000];


                var colorScale2 = d3.scale.threshold()
                    .domain(domain_data)
                    .range(colors);


                var legend2 = svgGE.selectAll(".legend")

                //.data([min_data, min_data + (max_data - min_data) / 7, min_data + 2 * (max_data - min_data) / 7, min_data + 3 * (max_data - min_data) / 7, min_data + 4 * (max_data - min_data) / 7, min_data + 5 * (max_data - min_data) / 7, min_data + 6 * (max_data - min_data) / 7], function (d) {
                    .data([-2.0, -1.6, -1.2, -0.8, -0.4, -0.01, 0.01, 0.4, 0.8, 1.2, 1.6, 2.0, 10.0], function (d) {

                        return d;
                    });

                // //console.log("colorScale.quantiles()");
                // //console.log(colorScale.quantiles());
                legend2.enter().append("g")
                    .attr("class", "legend");
                var gridSize = Math.floor(globalW / 40);
                var legendElementWidth = gridSize * 2;
                legend2.append("rect")
                    .attr("x", function (d, i) {
                        return legendElementWidth * i;
                    })
                    .attr("y", globalHPlus50 - 40)
                    .attr("width", legendElementWidth)
                    .attr("height", gridSize / 2)
                    .style("fill", function (d, i) {
                        return colors[i];
                    });

                legend2.append("text")
                //.attr("class", "mono")
                    .text(function (d, i) {
                        if (i == 0) {
                            return " a < " + parseFloat(Math.round(d * 100) / 100).toFixed(1);
                        }
                        else if (i == svgGE.selectAll(".legend").data().length - 1) {

                            return parseFloat(Math.round((svgGE.selectAll(".legend").data()[i - 1]) * 100) / 100).toFixed(1) + " ≤ a ";
                        }
                        else {

                            return parseFloat(Math.round((svgGE.selectAll(".legend").data()[i - 1]) * 100) / 100).toFixed(1) + " ≤ a < " + parseFloat(Math.round(d * 100) / 100).toFixed(1);
                        }
                        //return  parseFloat(Math.round(d * 100) / 100).toFixed(2) + "≥ a";
                    })
                    .style("font", "11px Times New Roman")
                    .attr("x", function (d, i) {
                        return legendElementWidth * i;
                    })
                    .attr("y", globalHPlus50 - 40 + gridSize);

                legend2.exit().remove();
            }


        };

        d3.select('#circosViewGE').on('click', function () {
            circosViewGE();
            self.graphType = 0;
        });


        function parallelViewGE() {
            svgGE.remove();

            //xPosition.domain(d3.extent(nodes, function (d) { return d.text; }));
            xScale.domain(d3.extent(nodes, function (d) {
                return d.weight;
            }));
            colNodeScale.domain(d3.extent(nodes, function (d) {
                return d.group;
            }));
            colScale.domain(d3.extent(links, function (d) {
                return d.weight;
            }));
            textPlacePlusMinus.domain(d3.extent(nodes, function (d) {
                return d.group;
            }));
            textPlaceStartEnd.domain(d3.extent(nodes, function (d) {
                return d.group;
            }));
            scoreScale.domain(d3.extent(links, function (d) {
                return d.score;
            }));

            var groupId = {};
            var groupIds = [];
            var maxId = 0;
            var maxGroupNum = 0;
            for (var i = 0; i < nodes.length; i++) {
                var item = nodes[i];

                if (!groupId[item.group]) {
                    groupId[item.group] = [];
                    groupIds.push(item.group);
                }

                groupId[item.group].push({name: item.name});
                // //console.log(item.group);
                // //console.log(groupId[item.group]);
                // if (maxId < item.group) {
                //     maxId = item.group;
                // }
            }
            //console.log(maxId);
            var nodeListIter = {};
            for (var key in groupId) {
                if (groupId.hasOwnProperty(key)) {
                    nodeListIter[key] = 0;
                    maxId += 1;
                    console.log(groupId[key]);
                    console.log(groupId[key].length);
                    if (maxGroupNum < groupId[key].length) {
                        maxGroupNum = groupId[key].length;
                    }
                }
            }
            console.log(groupIds);
            groupIds.sort();
            console.log(groupIds);

            console.log(maxId);
            console.log(maxGroupNum);

            var parallelH = Math.max(maxGroupNum * 25, 500);
            //var parallelH = Math.max(n1 * 12, n2 * 12);

            var margin = 75,
                w = widthSize - 2 * margin,
                h = parallelH,
                radius = w / 2,
                strokeWidth = 4,
                hyp2 = Math.pow(radius, 2),
                nodeBaseRad = 5;

            globalH = h;
            globalHPlus50 = h + 50;
            globalW = w;


            svgGE = d3.select("#chartGE")
                .append("svg")
                .attr("style", "outline: thin solid yellow;")
                .attr("width", w)
                .attr("height", globalHPlus50);

            svgGE.append("rect")
                .attr("width", "100%")
                .attr("height", "100%")
                .attr("fill", "white");


            var force = d3.layout.force()
                .nodes(nodes)
                .links(links)
                .size([w, h]);


            var parallelCoordx = function (group, maxId) {


                return group * w / (maxId + 1) + w / (maxId + 1);

            }

            var parallelCoordy = function (index, num_nodes) {
                var dist = h / (num_nodes + 1);

                return (index + 1) * dist;
            }

            var is_connected = function (d, opacity) {
                lines.transition().style("stroke-opacity", function (o) {
                    return o.source === d || o.target === d ? 1 : opacity;
                });
            }

            var is_connected_on_click = function (d, opacity) {
                //console.log(d);
                lines.transition().style("stroke-opacity", function (o) {
                    return o.source.group === d.group || o.target.group === d.group ? 1 : opacity;
                });
            }
            //var dim = w-80
            // var circle = svg.append("path")
            //     .attr("d", "M 40, "+(dim/2+40)+" a "+dim/2+","+dim/2+" 0 1,0 "+dim+",0 a "+dim/2+","+dim/2+" 0 1,0 "+dim*-1+",0")
            //     .style("fill", "#f5f5f5");

            force.start();


            // //console.log(nodes.length);


            nodes.forEach(function (n, i) {
                var groupOrder = groupIds.indexOf(n.group);
                n.x = parallelCoordx(groupOrder, maxId);
                n.y = parallelCoordy(nodeListIter[n.group], groupId[n.group].length);
                nodeListIter[n.group] += 1;

            });


            // use this one for straight line links...
            // var lines = svg.selectAll("line.node-link")
            //   .data(links).enter().append("line")
            //     .attr("class", "node-link")
            //   .attr("x1", function(d) { return d.source.x; })
            //   .attr("y1", function(d) { return d.source.y; })
            //   .attr("x2", function(d) { return d.target.x; })
            //   .attr("y2", function(d) { return d.target.y; });

            var lines = svgGE.selectAll("path.node-link")
                .data(links).enter().append("path")
                .style("fill", "none")
                .style("stroke", function (d) {

                    if (d.tag == 0) {
                        return ("#696969");
                    }
                    else if (d.tag == 1) {
                        return ("#006400");
                    }
                    else if (d.tag == 2) {
                        return ("#00FF00");
                    }
                    else if (d.tag == 3) {
                        return ("#0000FF");
                    }
                    else if (d.tag == 4) {
                        return ("#808080");
                    }
                    else if (d.tag == 5) {
                        return ("#8B4513");
                    }
                    else if (d.tag == 6) {
                        return ("#FFFFE0");
                    }
                    else if (d.tag == 7) {
                        return ("#8464c5");
                    }
                    else if (d.tag == 8) {
                        return ("#00FFFF");
                    }
                    else if (d.tag == 9) {
                        return ("#FF7F50");
                    }
                    else if (d.tag == 10) {
                        return ("#FF0000");
                    }
                    else if (d.tag == 11) {
                        return ("#FF00FF");
                    }
                    else if (d.tag == 12) {
                        return ("#8FBC8F");
                    }
                    else if (d.tag == 13) {
                        return ("#A52A2A");
                    }
                    else if (d.tag == 14) {
                        return ("#FFD700");
                    }
                    else if (d.tag == 15) {
                        return ("#A0522D");
                    }
                    else if (d.tag == 16) {
                        return ("#FFFF00");
                    }
                    else if (d.tag == 17) {
                        return ("#6A5ACD");
                    }
                    else if (d.tag == 18) {
                        return ("#708090");
                    }
                    else if (d.tag == 19) {
                        return ("#FF6347");
                    }
                    else if (d.tag == 20) {
                        return ("#CD5C5C");
                    }
                    else if (d.tag == 21) {
                        return ("#DB7093");
                    }
                    else if (d.tag == 22) {
                        return ("#2E8B57");
                    }
                    else if (d.tag == 23) {
                        return ("#000080");
                    }
                    else if (d.tag == 24) {
                        return ("#9370DB");
                    }
                    else if (d.tag == 25) {
                        return ("#A52A2A");
                    }
                    else if (d.tag == 26) {
                        return ("#FDF5E6");
                    }
                    else if (d.tag == 27) {
                        return ("#7B68EE");
                    }
                    else if (d.tag == 28) {
                        return ("#696969");
                    }
                    else if (d.tag == 29) {
                        return ("#FF4500");
                    }
                    else if (d.tag == 30) {
                        return ("#DC143C");
                    }
                    else if (d.tag == 31) {
                        return ("#FF69B4");
                    }
                    else if (d.tag == 32) {
                        return ("#006400");
                    }
                    else if (d.tag == 33) {
                        return ("#87CEEB");
                    }
                    else if (d.tag == 34) {
                        return ("#EE82EE");
                    }
                    else if (d.tag == 35) {
                        return ("#800000");
                    }
                    else if (d.tag == 36) {
                        return ("#FAEBD7");
                    }
                    else if (d.tag == 37) {
                        return ("#4B0082");
                    }
                    else if (d.tag == 38) {
                        return ("#808080");
                    }
                    else if (d.tag == 39) {
                        return ("#FF8C00");
                    }
                    else if (d.tag == 40) {
                        return ("#FA8072");
                    }
                    else if (d.tag == 41) {
                        return ("#FFC0CB");
                    }
                    else if (d.tag == 42) {
                        return ("#9ACD32");
                    }
                    else if (d.tag == 43) {
                        return ("#4682B4");
                    }
                    else if (d.tag == 44) {
                        return ("#DDA0DD");
                    }
                    else if (d.tag == 45) {
                        return ("#CD853F");
                    }
                    else if (d.tag == 46) {
                        return ("#FFE4E1");
                    }
                    else if (d.tag == 47) {
                        return ("#696969");
                    }
                    else if (d.tag == 48) {
                        return ("#A9A9A9");
                    }
                    else if (d.tag == 49) {
                        return ("#FFA500");
                    }
                    else {
                        return ("#000000");
                    }


                    // if (d.group == 0) {
                    //     return colorScale(d.value);
                    // }
                    // else {
                    //
                    //     if (d.group == 1) {
                    //         return("#ed0909");
                    //     }
                    //     if (d.group == 2) {
                    //         return("#0af702");
                    //     }
                    //     if (d.group == 3) {
                    //         return("#FF00FF");
                    //     }
                    //     if (d.group == 4) {
                    //         return("#808000");
                    //     }
                    //     if (d.group == 5) {
                    //         return("#000080");
                    //     }
                    //     if (d.group == 6) {
                    //         return("#800080");
                    //     }
                    //     if (d.group == 7) {
                    //         return("#00ffff");
                    //     }
                    //     if (d.group == 8) {
                    //         return("#F5F5DC");
                    //     }
                    //     if (d.group == 9) {
                    //         return("#A52A2A");
                    //     }
                    //     if (d.group == 10) {
                    //         return("#8B0000");
                    //     }
                    //     if (d.group == 11) {
                    //         return("#FF8C00");
                    //     }
                    //
                    // }

                })
                //.style("stroke", "#726363")
                .attr("class", "node-link")
                .style("stroke-width", function (d) {
                    return d.score / 2;
                })
                .attr("d", function (d) {

                    var dx = d.target.x - d.source.x,
                        dy = d.target.y - d.source.y,
                        dr = Math.sqrt(dx * dx + dy * dy),
                        a1 = dx,
                        a2 = dy,
                        c1 = w / 2 - d.source.x,
                        c2 = h / 2 - d.source.y,
                        d1 = w / 2 - d.target.x,
                        d2 = h / 2 - d.target.y,

                        drx = dr / 1.5,
                        dry = dr / 1.5,
                        xRotation = 0, // degrees
                        largeArc = 0, // 1 or 0

                        sweep = 1, // 1 or 0
                        x2 = d.target.x,
                        y2 = d.target.y;


                    // if( (a1*c2 - a2*c1) > 0)
                    // {
                    //     sweep = 0
                    // }
                    // else
                    // {sweep = 1}
                    if ((c1 * d2 - c2 * d1) > 0) {
                        sweep = 0
                    }
                    else {
                        sweep = 1
                    }


                    return "M" + d.source.x + "," + d.source.y + "A" + drx + "," + dry + " " + xRotation + "," + largeArc + "," + sweep + " " + x2 + "," + y2;


                    //return "M" + d.source.x + "," + d.source.y + ","+ d.target.x + "," + d.target.y;
                    //return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
                });
            // .attr("d", function (d) {
            //     var dx = d.target.x - d.source.x,
            //         dy = d.target.y - d.source.y,
            //         dr = Math.sqrt(dx * dx + dy * dy);
            //     return "M" +
            //         d.source.x + "," +
            //         d.source.y + "," +
            //         d.target.x + "," +
            //         d.target.y;
            // });


            // nodes.weight = lines.filter(function(l) {
            //     return l.source.index == d.index || l.target.index == d.index
            // }).size();

            // var lines = svg.selectAll("path.node-link")
            //     .data(links).enter().append("path")
            //     .style("fill", "none")
            //     .style("stroke", "black")
            //     .attr("class", "node-link")
            //     .attr("d", function(d) {
            //         var dx = d.target.x - d.source.x,
            //             dy = d.target.y - d.source.y,
            //             dr = Math.sqrt(dx * dx + dy * dy);
            //         return "M" +
            //             d.source.x + "," +
            //             d.source.y + "A" +
            //             dr + "," + dr + " 0 0,1 " +
            //             d.target.x + "," +
            //             d.target.y;
            //     });

            var gnodes = svgGE.selectAll('g.gnode')
                .data(nodes).enter().append('g')
                .attr("transform", function (d) {
                    return "translate(" + d.x + "," + d.y + ")"
                })
                .classed('gnode', true);

            // gnodes.forEach(function (n, i) {
            //     n.weight = lines.filter(function (l) {
            //         return l.source.idx == n.idx || l.target.idx == n.idx
            //     }).size();
            //
            // });
            var node = gnodes.append("circle")
            //.attr("r", function(d) {
            // d.sizes = lines.filter(function(l) {
            //     return l.source.index == d.index || l.target.index == d.index
            // }).size();
            // var minRadius = 5;
            // return minRadius + (d.sizes * 2);
            //     return colorScale(d.weight);
            // })
                .attr("r", function (d) {
                    return xScale(d.weight);
                })
                .style("fill", function (d) {

                    if (d.group == 0) {
                        return ("#696969");
                    }
                    else if (d.group == 1) {
                        return ("#006400");
                    }
                    else if (d.group == 2) {
                        return ("#00FF00");
                    }
                    else if (d.group == 3) {
                        return ("#0000FF");
                    }
                    else if (d.group == 4) {
                        return ("#808080");
                    }
                    else if (d.group == 5) {
                        return ("#8B4513");
                    }
                    else if (d.group == 6) {
                        return ("#FFFFE0");
                    }
                    else if (d.group == 7) {
                        return ("#8464c5");
                    }
                    else if (d.group == 8) {
                        return ("#00FFFF");
                    }
                    else if (d.group == 9) {
                        return ("#FF7F50");
                    }
                    else if (d.group == 10) {
                        return ("#FF0000");
                    }
                    else if (d.group == 11) {
                        return ("#FF00FF");
                    }
                    else if (d.group == 12) {
                        return ("#8FBC8F");
                    }
                    else if (d.group == 13) {
                        return ("#A52A2A");
                    }
                    else if (d.group == 14) {
                        return ("#FFD700");
                    }
                    else if (d.group == 15) {
                        return ("#A0522D");
                    }
                    else if (d.group == 16) {
                        return ("#FFFF00");
                    }
                    else if (d.group == 17) {
                        return ("#6A5ACD");
                    }
                    else if (d.group == 18) {
                        return ("#708090");
                    }
                    else if (d.group == 19) {
                        return ("#FF6347");
                    }
                    else if (d.group == 20) {
                        return ("#CD5C5C");
                    }
                    else if (d.group == 21) {
                        return ("#DB7093");
                    }
                    else if (d.group == 22) {
                        return ("#2E8B57");
                    }
                    else if (d.group == 23) {
                        return ("#000080");
                    }
                    else if (d.group == 24) {
                        return ("#9370DB");
                    }
                    else if (d.group == 25) {
                        return ("#A52A2A");
                    }
                    else if (d.group == 26) {
                        return ("#FDF5E6");
                    }
                    else if (d.group == 27) {
                        return ("#7B68EE");
                    }
                    else if (d.group == 28) {
                        return ("#696969");
                    }
                    else if (d.group == 29) {
                        return ("#FF4500");
                    }
                    else if (d.group == 30) {
                        return ("#DC143C");
                    }
                    else if (d.group == 31) {
                        return ("#FF69B4");
                    }
                    else if (d.group == 32) {
                        return ("#006400");
                    }
                    else if (d.group == 33) {
                        return ("#87CEEB");
                    }
                    else if (d.group == 34) {
                        return ("#EE82EE");
                    }
                    else if (d.group == 35) {
                        return ("#800000");
                    }
                    else if (d.group == 36) {
                        return ("#FAEBD7");
                    }
                    else if (d.group == 37) {
                        return ("#4B0082");
                    }
                    else if (d.group == 38) {
                        return ("#808080");
                    }
                    else if (d.group == 39) {
                        return ("#FF8C00");
                    }
                    else if (d.group == 40) {
                        return ("#FA8072");
                    }
                    else if (d.group == 41) {
                        return ("#FFC0CB");
                    }
                    else if (d.group == 42) {
                        return ("#9ACD32");
                    }
                    else if (d.group == 43) {
                        return ("#4682B4");
                    }
                    else if (d.group == 44) {
                        return ("#DDA0DD");
                    }
                    else if (d.group == 45) {
                        return ("#CD853F");
                    }
                    else if (d.group == 46) {
                        return ("#FFE4E1");
                    }
                    else if (d.group == 47) {
                        return ("#696969");
                    }
                    else if (d.group == 48) {
                        return ("#A9A9A9");
                    }
                    else if (d.group == 49) {
                        return ("#FFA500");
                    }
                    else {
                        return ("#000000");
                    }


                    // if (d.group == 0) {
                    //     return colorScale(d.value);
                    // }
                    // else {
                    //
                    //     if (d.group == 1) {
                    //         return("#ed0909");
                    //     }
                    //     if (d.group == 2) {
                    //         return("#0af702");
                    //     }
                    //     if (d.group == 3) {
                    //         return("#FF00FF");
                    //     }
                    //     if (d.group == 4) {
                    //         return("#808000");
                    //     }
                    //     if (d.group == 5) {
                    //         return("#000080");
                    //     }
                    //     if (d.group == 6) {
                    //         return("#800080");
                    //     }
                    //     if (d.group == 7) {
                    //         return("#00ffff");
                    //     }
                    //     if (d.group == 8) {
                    //         return("#F5F5DC");
                    //     }
                    //     if (d.group == 9) {
                    //         return("#A52A2A");
                    //     }
                    //     if (d.group == 10) {
                    //         return("#8B0000");
                    //     }
                    //     if (d.group == 11) {
                    //         return("#FF8C00");
                    //     }
                    //
                    // }

                })

                // .style("fill", function (d) {
                //     return colNodeScale(d.group);
                // })
                .style("stroke", "#333")
                .style("stroke-width", "2px")
                .style("stroke-dasharray",
                    function (d) {
                        if (d.connected == "No") {
                            ////console.log("not connected");
                            return (5, 5);

                        }
                        else if (d.connected == "Yes") {
                            ////console.log("connected");
                            return (3, 0);
                        }
                    })
                //.attr("class", "node")
                .on("mouseenter", function (d) {
                    is_connected(d, 0.1)
                    node.transition().duration(100).attr("r", function (d) {
                        return xScale(d.weight);
                    })
                    d3.select(this).transition().duration(100).attr("r", function (d) {
                        return xScale(d.weight + 3);
                    })
                })
                // .on("mouseleave", function (d) {
                //     node.transition().duration(100).attr("r", function (d) {
                //         return xScale(d.weight);
                //     })
                //     is_connected(d, 1);
                // })
                .on("click", function (d) {

                    //if(!first_click) {
                    is_connected_on_click(d, 0.1);
                    node.transition().duration(100).attr("r", function (d) {
                        return xScale(d.weight);
                    })
                    d3.select(this).transition().duration(100).attr("r", function (d) {
                        return xScale(d.weight + 3);
                    })

                })
                .call(force.drag);
            // var bbox = textElement.getBBox();
            // var width = bbox.width;
            // var height = bbox.height;
            var labels = gnodes.append("text")
                .style("font", String(fontSize) + "px Arial")
                .attr("dx", function (d) {
                    return -18;
                })
                .attr("dy", 4)
                .attr("text-anchor", function (d) {
                    return "end";
                })
                .text(function (d) {
                    return d.full_name
                })

            var svgText = svgGE.append("text");
            svgText.attr("x", 10).attr("y", globalHPlus50 - 50).text("PiNET-server @ www.pinet-server.org").style("font", "14px Times New Roman");
            if (1 == 0) {
                //Added from here for coloring the legend
                max_data = 1000;
                min_data = -1000;


                var colors = ["#00A6FF", "#1097E0", "#2885B7", "#35799E", "#4C7991", "#6D828D", "#8C8C8C", "#8E8E5C", "#92923C", "#A5A52E", "#BDBD24", "#DDDD15", "#FFFF00"];
                var domain_data = [-2.0, -1.6, -1.2, -0.8, -0.4, -0.01, 0.01, 0.4, 0.8, 1.2, 1.6, 2.0, 1000];


                var colorScale2 = d3.scale.threshold()
                    .domain(domain_data)
                    .range(colors);


                var legend2 = svgGE.selectAll(".legend")

                //.data([min_data, min_data + (max_data - min_data) / 7, min_data + 2 * (max_data - min_data) / 7, min_data + 3 * (max_data - min_data) / 7, min_data + 4 * (max_data - min_data) / 7, min_data + 5 * (max_data - min_data) / 7, min_data + 6 * (max_data - min_data) / 7], function (d) {
                    .data([-2.0, -1.6, -1.2, -0.8, -0.4, -0.01, 0.01, 0.4, 0.8, 1.2, 1.6, 2.0, 10.0], function (d) {

                        return d;
                    });

                // //console.log("colorScale.quantiles()");
                // //console.log(colorScale.quantiles());
                legend2.enter().append("g")
                    .attr("class", "legend");
                var gridSize = Math.floor(globalW / 40);
                var legendElementWidth = gridSize * 2;
                legend2.append("rect")
                    .attr("x", function (d, i) {
                        return legendElementWidth * i;
                    })
                    .attr("y", globalHPlus50 - 40)
                    .attr("width", legendElementWidth)
                    .attr("height", gridSize / 2)
                    .style("fill", function (d, i) {
                        return colors[i];
                    });

                legend2.append("text")
                //.attr("class", "mono")
                    .text(function (d, i) {
                        if (i == 0) {
                            return " a < " + parseFloat(Math.round(d * 100) / 100).toFixed(1);
                        }
                        else if (i == svgGE.selectAll(".legend").data().length - 1) {

                            return parseFloat(Math.round((svgGE.selectAll(".legend").data()[i - 1]) * 100) / 100).toFixed(1) + " ≤ a ";
                        }
                        else {

                            return parseFloat(Math.round((svgGE.selectAll(".legend").data()[i - 1]) * 100) / 100).toFixed(1) + " ≤ a < " + parseFloat(Math.round(d * 100) / 100).toFixed(1);
                        }
                        //return  parseFloat(Math.round(d * 100) / 100).toFixed(2) + "≥ a";
                    })
                    .style("font", "11px Times New Roman")
                    .attr("x", function (d, i) {
                        return legendElementWidth * i;
                    })
                    .attr("y", globalHPlus50 - 40 + gridSize);
                legend2.exit().remove();
            }
            //legend2.exit().remove();

            //till here for coloring the legend

        };


        d3.select('#parallelViewGE').on('click', function () {
            parallelViewGE();
            self.graphType = 2;
        });


        function defaultSVGGE() {


            svgGE.remove();

            xScale.domain(d3.extent(nodes, function (d) {
                return d.weight;
            }));
            colNodeScale.domain(d3.extent(nodes, function (d) {
                return d.group;
            }));
            // colorScale.domain(d3.extent(nodes, function (d) {
            //     return d.value;
            // }));
            colScale.domain(d3.extent(links, function (d) {
                return d.weight;
            }));
            scoreScale.domain(d3.extent(links, function (d) {
                return d.score;
            }));
            var margin = 75,
                w = widthSize - 2 * margin,
                h = w,
                radius = w / 2,
                strokeWidth = 4,
                hyp2 = Math.pow(radius, 2),
                nodeBaseRad = 5;

//These variables are global variables
            globalH = h;
            globalHPlus50 = h + 50;
            globalW = w;

            svgGE = d3.select("#chartGE")
                .append("svg")
                .attr("style", "outline: thin solid yellow;")
                .attr("width", w)
                .attr("height", globalHPlus50);
            svgGE.append("rect")
                .attr("width", "100%")
                .attr("height", "100%")
                .attr("fill", "white");


            var force = d3.layout.force()
                .nodes(nodes)
                .links(links)
                .size([w, h])
                .linkDistance(350)
                .charge(-2000)
                //.linkStrength(0.9)
                //.friction(0.9)
                //.chargeDistance(300)
                .gravity(0.15)
                //.theta(0.8)
                //.alpha(0.1)
                .on("tick", tick)
                .start();

            // for (var i = n*n; i > 0; --i) force.tick();
            // force.stop();

            //.stop();


            var path = svgGE.append("svg:g").selectAll("path")
            //.data(links)
                .data(force.links())
                .enter().append("svg:path")
                .style("stroke-width", function (d) {
                    return d.score / 2;
                })

                .style("stroke", function (d) {


                    if (d.tag == 0) {
                        return ("#696969");
                    }

                    else if (d.tag == 1) {
                        return ("#006400");
                    }
                    else if (d.tag == 2) {
                        return ("#00FF00");
                    }
                    else if (d.tag == 3) {
                        return ("#0000FF");
                    }
                    else if (d.tag == 4) {
                        return ("#808080");
                    }
                    else if (d.tag == 5) {
                        return ("#8B4513");
                    }
                    else if (d.tag == 6) {
                        return ("#FFFFE0");
                    }
                    else if (d.tag == 7) {
                        return ("#8464c5");
                    }
                    else if (d.tag == 8) {
                        return ("#00FFFF");
                    }
                    else if (d.tag == 9) {
                        return ("#FF7F50");
                    }
                    else if (d.tag == 10) {
                        return ("#FF0000");
                    }
                    else if (d.tag == 11) {
                        return ("#FF00FF");
                    }
                    else if (d.tag == 12) {
                        return ("#8FBC8F");
                    }
                    else if (d.tag == 13) {
                        return ("#A52A2A");
                    }
                    else if (d.tag == 14) {
                        return ("#FFD700");
                    }
                    else if (d.tag == 15) {
                        return ("#A0522D");
                    }
                    else if (d.tag == 16) {
                        return ("#FFFF00");
                    }
                    else if (d.tag == 17) {
                        return ("#6A5ACD");
                    }
                    else if (d.tag == 18) {
                        return ("#708090");
                    }
                    else if (d.tag == 19) {
                        return ("#FF6347");
                    }
                    else if (d.tag == 20) {
                        return ("#CD5C5C");
                    }
                    else if (d.tag == 21) {
                        return ("#DB7093");
                    }
                    else if (d.tag == 22) {
                        return ("#2E8B57");
                    }
                    else if (d.tag == 23) {
                        return ("#000080");
                    }
                    else if (d.tag == 24) {
                        return ("#9370DB");
                    }
                    else if (d.tag == 25) {
                        return ("#A52A2A");
                    }
                    else if (d.tag == 26) {
                        return ("#FDF5E6");
                    }
                    else if (d.tag == 27) {
                        return ("#7B68EE");
                    }
                    else if (d.tag == 28) {
                        return ("#696969");
                    }
                    else if (d.tag == 29) {
                        return ("#FF4500");
                    }
                    else if (d.tag == 30) {
                        return ("#DC143C");
                    }
                    else if (d.tag == 31) {
                        return ("#FF69B4");
                    }
                    else if (d.tag == 32) {
                        return ("#006400");
                    }
                    else if (d.tag == 33) {
                        return ("#87CEEB");
                    }
                    else if (d.tag == 34) {
                        return ("#EE82EE");
                    }
                    else if (d.tag == 35) {
                        return ("#800000");
                    }
                    else if (d.tag == 36) {
                        return ("#FAEBD7");
                    }
                    else if (d.tag == 37) {
                        return ("#4B0082");
                    }
                    else if (d.tag == 38) {
                        return ("#808080");
                    }
                    else if (d.tag == 39) {
                        return ("#FF8C00");
                    }
                    else if (d.tag == 40) {
                        return ("#FA8072");
                    }
                    else if (d.tag == 41) {
                        return ("#FFC0CB");
                    }
                    else if (d.tag == 42) {
                        return ("#9ACD32");
                    }
                    else if (d.tag == 43) {
                        return ("#4682B4");
                    }
                    else if (d.tag == 44) {
                        return ("#DDA0DD");
                    }
                    else if (d.tag == 45) {
                        return ("#CD853F");
                    }
                    else if (d.tag == 46) {
                        return ("#FFE4E1");
                    }
                    else if (d.tag == 47) {
                        return ("#696969");
                    }
                    else if (d.tag == 48) {
                        return ("#A9A9A9");
                    }
                    else if (d.tag == 49) {
                        return ("#FFA500");
                    }
                    else {
                        return ("#000000");
                    }


                    // if (d.group == 0) {
                    //     return colorScale(d.value);
                    // }
                    // else {
                    //
                    //     if (d.group == 1) {
                    //         return("#ed0909");
                    //     }
                    //     if (d.group == 2) {
                    //         return("#0af702");
                    //     }
                    //     if (d.group == 3) {
                    //         return("#FF00FF");
                    //     }
                    //     if (d.group == 4) {
                    //         return("#808000");
                    //     }
                    //     if (d.group == 5) {
                    //         return("#000080");
                    //     }
                    //     if (d.group == 6) {
                    //         return("#800080");
                    //     }
                    //     if (d.group == 7) {
                    //         return("#00ffff");
                    //     }
                    //     if (d.group == 8) {
                    //         return("#F5F5DC");
                    //     }
                    //     if (d.group == 9) {
                    //         return("#A52A2A");
                    //     }
                    //     if (d.group == 10) {
                    //         return("#8B0000");
                    //     }
                    //     if (d.group == 11) {
                    //         return("#FF8C00");
                    //     }
                    //
                    // }

                })

                //.style('stroke', "black")
                //.style("stroke", function (d) {return colScale(d.value); })
                .attr("class", function (d) {
                    return "link ";
                });


            var node = svgGE.append("svg:g").selectAll("g.node")
                .data(force.nodes())
                .enter().append("svg:g")
                // .style("stroke-width", 3)
                // .style('stroke', "black")
                //.attr("class", "node")
                .call(force.drag);

            // nodes.forEach(function(v) {
            //     var nd;
            //     var cx = v.coord[0];
            //     var cy = v.coord[1];
            //
            //     switch (v.group) {
            //         case 1:
            //             nd = svg.append("circle");
            //             break;
            //         case 2:
            //             nd = svg.append("rect");
            //             break;
            //     }
            // });


            var colorsForAbundance = ["#00A6FF", "#1097E0", "#2885B7", "#35799E", "#4C7991", "#6D828D", "#8C8C8C", "#8E8E5C", "#92923C", "#A5A52E", "#BDBD24", "#DDDD15", "#FFFF00"];
            var domain_data = [-2.0, -1.6, -1.2, -0.8, -0.4, -0.01, 0.01, 0.4, 0.8, 1.2, 1.6, 2.0, 1000];
            var colorScale = d3.scale.threshold()
                .domain(domain_data)
                .range(colorsForAbundance);


            node.append("circle")
                .attr("r", function (d) {
                    return xScale(d.weight);
                })
                .style("fill", function (d) {

                    if (d.group == 0) {
                        return ("#696969");
                    }
                    else if (d.group == 1) {
                        return ("#006400");
                    }
                    else if (d.group == 2) {
                        return ("#00FF00");
                    }
                    else if (d.group == 3) {
                        return ("#0000FF");
                    }
                    else if (d.group == 4) {
                        return ("#808080");
                    }
                    else if (d.group == 5) {
                        return ("#8B4513");
                    }
                    else if (d.group == 6) {
                        return ("#FFFFE0");
                    }
                    else if (d.group == 7) {
                        return ("#8464c5");
                    }
                    else if (d.group == 8) {
                        return ("#00FFFF");
                    }
                    else if (d.group == 9) {
                        return ("#FF7F50");
                    }
                    else if (d.group == 10) {
                        return ("#FF0000");
                    }
                    else if (d.group == 11) {
                        return ("#FF00FF");
                    }
                    else if (d.group == 12) {
                        return ("#8FBC8F");
                    }
                    else if (d.group == 13) {
                        return ("#A52A2A");
                    }
                    else if (d.group == 14) {
                        return ("#FFD700");
                    }
                    else if (d.group == 15) {
                        return ("#A0522D");
                    }
                    else if (d.group == 16) {
                        return ("#FFFF00");
                    }
                    else if (d.group == 17) {
                        return ("#6A5ACD");
                    }
                    else if (d.group == 18) {
                        return ("#708090");
                    }
                    else if (d.group == 19) {
                        return ("#FF6347");
                    }
                    else if (d.group == 20) {
                        return ("#CD5C5C");
                    }
                    else if (d.group == 21) {
                        return ("#DB7093");
                    }
                    else if (d.group == 22) {
                        return ("#2E8B57");
                    }
                    else if (d.group == 23) {
                        return ("#000080");
                    }
                    else if (d.group == 24) {
                        return ("#9370DB");
                    }
                    else if (d.group == 25) {
                        return ("#A52A2A");
                    }
                    else if (d.group == 26) {
                        return ("#FDF5E6");
                    }
                    else if (d.group == 27) {
                        return ("#7B68EE");
                    }
                    else if (d.group == 28) {
                        return ("#696969");
                    }
                    else if (d.group == 29) {
                        return ("#FF4500");
                    }
                    else if (d.group == 30) {
                        return ("#DC143C");
                    }
                    else if (d.group == 31) {
                        return ("#FF69B4");
                    }
                    else if (d.group == 32) {
                        return ("#006400");
                    }
                    else if (d.group == 33) {
                        return ("#87CEEB");
                    }
                    else if (d.group == 34) {
                        return ("#EE82EE");
                    }
                    else if (d.group == 35) {
                        return ("#800000");
                    }
                    else if (d.group == 36) {
                        return ("#FAEBD7");
                    }
                    else if (d.group == 37) {
                        return ("#4B0082");
                    }
                    else if (d.group == 38) {
                        return ("#808080");
                    }
                    else if (d.group == 39) {
                        return ("#FF8C00");
                    }
                    else if (d.group == 40) {
                        return ("#FA8072");
                    }
                    else if (d.group == 41) {
                        return ("#FFC0CB");
                    }
                    else if (d.group == 42) {
                        return ("#9ACD32");
                    }
                    else if (d.group == 43) {
                        return ("#4682B4");
                    }
                    else if (d.group == 44) {
                        return ("#DDA0DD");
                    }
                    else if (d.group == 45) {
                        return ("#CD853F");
                    }
                    else if (d.group == 46) {
                        return ("#FFE4E1");
                    }
                    else if (d.group == 47) {
                        return ("#696969");
                    }
                    else if (d.group == 48) {
                        return ("#A9A9A9");
                    }
                    else if (d.group == 49) {
                        return ("#FFA500");
                    }

                    else if (d.group == 117) {
                        return ("#FFD600FF");
                    }
                    else if (d.group == 64) {
                        return ("#FF7600FF");
                    }
                    else if (d.group == 85) {
                        return ("#FFFF9CFF");
                    }
                    else if (d.group == 95) {
                        return ("#FF3000FF");
                    }
                    else if (d.group == 123) {
                        return ("#FFFF0BFF");
                    }
                    else if (d.group == 88) {
                        return ("#FFFFF1FF");
                    }
                    else if (d.group == 73) {
                        return ("#FFC800FF");
                    }
                    else if (d.group == 118) {
                        return ("#FFDD00FF");
                    }
                    else if (d.group == 129) {
                        return ("#FFFF8AFF");
                    }
                    else if (d.group == 54) {
                        return ("#FF1B00FF");
                    }
                    else if (d.group == 122) {
                        return ("#FFF800FF");
                    }
                    else if (d.group == 130) {
                        return ("#FFFF9FFF");
                    }
                    else if (d.group == 99) {
                        return ("#FF5300FF");
                    }
                    else if (d.group == 98) {
                        return ("#FF4C00FF");
                    }
                    else if (d.group == 56) {
                        return ("#FF2E00FF");
                    }
                    else if (d.group == 89) {
                        return ("#FF0700FF");
                    }
                    else if (d.group == 110) {
                        return ("#FF9F00FF");
                    }
                    else if (d.group == 101) {
                        return ("#FF6000FF");
                    }
                    else if (d.group == 93) {
                        return ("#FF2200FF");
                    }
                    else if (d.group == 53) {
                        return ("#FF1200FF");
                    }
                    else if (d.group == 108) {
                        return ("#FF9100FF");
                    }
                    else if (d.group == 69) {
                        return ("#FFA400FF");
                    }
                    else if (d.group == 75) {
                        return ("#FFDB00FF");
                    }
                    else if (d.group == 76) {
                        return ("#FFE400FF");
                    }
                    else if (d.group == 119) {
                        return ("#FFE300FF");
                    }
                    else if (d.group == 134) {
                        return ("#FFFFF4FF");
                    }
                    else if (d.group == 62) {
                        return ("#FF6400FF");
                    }
                    else if (d.group == 127) {
                        return ("#FFFF60FF");
                    }
                    else if (d.group == 121) {
                        return ("#FFF100FF");
                    }
                    else if (d.group == 109) {
                        return ("#FF9800FF");
                    }
                    else if (d.group == 116) {
                        return ("#FFCF00FF");
                    }
                    else if (d.group == 124) {
                        return ("#FFFF20FF");
                    }
                    else if (d.group == 131) {
                        return ("#FFFFB5FF");
                    }
                    else if (d.group == 90) {
                        return ("#FF0E00FF");
                    }
                    else if (d.group == 114) {
                        return ("#FFBA00FF");
                    }
                    else if (d.group == 72) {
                        return ("#FFBF00FF");
                    }
                    else if (d.group == 52) {
                        return ("#FF0900FF");
                    }
                    else if (d.group == 63) {
                        return ("#FF6D00FF");
                    }
                    else if (d.group == 79) {
                        return ("#FFFF00FF");
                    }
                    else if (d.group == 80) {
                        return ("#FFFF0EFF");
                    }
                    else if (d.group == 78) {
                        return ("#FFF600FF");
                    }
                    else if (d.group == 107) {
                        return ("#FF8A00FF");
                    }
                    else if (d.group == 87) {
                        return ("#FFFFD4FF");
                    }
                    else if (d.group == 59) {
                        return ("#FF4900FF");
                    }
                    else if (d.group == 55) {
                        return ("#FF2400FF");
                    }
                    else if (d.group == 106) {
                        return ("#FF8300FF");
                    }
                    else if (d.group == 113) {
                        return ("#FFB300FF");
                    }
                    else if (d.group == 51) {
                        return ("#FF0000FF");
                    }
                    else if (d.group == 74) {
                        return ("#FFD100FF");
                    }
                    else if (d.group == 82) {
                        return ("#FFFF47FF");
                    }
                    else if (d.group == 104) {
                        return ("#FF7500FF");
                    }
                    else if (d.group == 66) {
                        return ("#FF8900FF");
                    }
                    else if (d.group == 133) {
                        return ("#FFFFDFFF");
                    }
                    else if (d.group == 86) {
                        return ("#FFFFB8FF");
                    }
                    else if (d.group == 65) {
                        return ("#FF8000FF");
                    }
                    else if (d.group == 132) {
                        return ("#FFFFCAFF");
                    }
                    else if (d.group == 58) {
                        return ("#FF4000FF");
                    }
                    else if (d.group == 105) {
                        return ("#FF7C00FF");
                    }
                    else if (d.group == 102) {
                        return ("#FF6700FF");
                    }
                    else if (d.group == 96) {
                        return ("#FF3E00FF");
                    }
                    else if (d.group == 125) {
                        return ("#FFFF35FF");
                    }
                    else if (d.group == 81) {
                        return ("#FFFF2BFF");
                    }
                    else if (d.group == 83) {
                        return ("#FFFF63FF");
                    }
                    else if (d.group == 120) {
                        return ("#FFEA00FF");
                    }
                    else if (d.group == 71) {
                        return ("#FFB600FF");
                    }
                    else if (d.group == 67) {
                        return ("#FF9200FF");
                    }
                    else if (d.group == 97) {
                        return ("#FF4500FF");
                    }
                    else if (d.group == 112) {
                        return ("#FFAC00FF");
                    }
                    else if (d.group == 61) {
                        return ("#FF5B00FF");
                    }
                    else if (d.group == 91) {
                        return ("#FF1500FF");
                    }
                    else if (d.group == 115) {
                        return ("#FFC100FF");
                    }
                    else if (d.group == 103) {
                        return ("#FF6E00FF");
                    }
                    else if (d.group == 70) {
                        return ("#FFAD00FF");
                    }
                    else if (d.group == 84) {
                        return ("#FFFF80FF");
                    }
                    else if (d.group == 126) {
                        return ("#FFFF4AFF");
                    }
                    else if (d.group == 100) {
                        return ("#FF5A00FF");
                    }
                    else if (d.group == 77) {
                        return ("#FFED00FF");
                    }
                    else if (d.group == 68) {
                        return ("#FF9B00FF");
                    }
                    else if (d.group == 57) {
                        return ("#FF3700FF");
                    }
                    else if (d.group == 92) {
                        return ("#FF1C00FF");
                    }
                    else if (d.group == 60) {
                        return ("#FF5200FF");
                    }
                    else if (d.group == 111) {
                        return ("#FFA500FF");
                    }
                    else if (d.group == 94) {
                        return ("#FF2900FF");
                    }
                    else if (d.group == 128) {
                            return ("#FFFF75FF");
                        }
                        else {
                            return ("#000000");
                        }


                    // if (d.group == 0) {
                    //     return colorScale(d.value);
                    // }
                    // else {
                    //
                    //     if (d.group == 1) {
                    //         return("#ed0909");
                    //     }
                    //     if (d.group == 2) {
                    //         return("#0af702");
                    //     }
                    //     if (d.group == 3) {
                    //         return("#FF00FF");
                    //     }
                    //     if (d.group == 4) {
                    //         return("#808000");
                    //     }
                    //     if (d.group == 5) {
                    //         return("#000080");
                    //     }
                    //     if (d.group == 6) {
                    //         return("#800080");
                    //     }
                    //     if (d.group == 7) {
                    //         return("#00ffff");
                    //     }
                    //     if (d.group == 8) {
                    //         return("#F5F5DC");
                    //     }
                    //     if (d.group == 9) {
                    //         return("#A52A2A");
                    //     }
                    //     if (d.group == 10) {
                    //         return("#8B0000");
                    //     }
                    //     if (d.group == 11) {
                    //         return("#FF8C00");
                    //     }
                    //
                    // }

                })

                // .style("fill", function (d) {
                //     return colNodeScale(d.group);
                // })
                .style("stroke", "#333")
                .style("stroke-dasharray",
                    function (d) {
                        if (d.connected == "No") {
                            ////console.log("not connected");
                            return (5, 5);

                        }
                        else if (d.connected == "Yes") {
                            ////console.log("connected");
                            return (3, 0);
                        }
                    })
                .style("stroke-width", "2px");
            //.on("dblclick", dblclick);


            // node.append("circle")
            //     .attr("r", function (d) {
            //         return xScale(d.weight);
            //     })
            //     .style("fill", function (d) {
            //         if (d.group == 1) {
            //             return colorScale(d.value);
            //         }
            //         else {
            //             return colNodeScale(d.group);
            //         }
            //         //return colNodeScale(d.group);
            //     })
            //     .style("stroke", "#333")
            //     .style("stroke-width", "2px");


            function openLink() {
                return function (d) {
                    var url = "";
                    if (d.slug != "") {
                        url = d.slug
                    } //else if(d.type == 2) {
                    //url = "clients/" + d.slug
                    //} else if(d.type == 3) {
                    //url = "agencies/" + d.slug
                    //}
                    window.open("//" + url)
                }
            };
            node.append("svg:image")
            //****************************************
            //.attr("class", function(d){ return d.name })
            //****************************************
            //.attr("xlink:href", function(d){ return d.img_hrefD})
                .attr("x", "-36px")
                .attr("y", "-36px")
                .attr("width", "70px")
                .attr("height", "70px")
            //.on("dblclick", openLink());

            // .on("mouseover", function (d) { if(d.entity == "company")
            // {
            //     d3.select(this).attr("width", "90px")
            //         .attr("x", "-46px")
            //         .attr("y", "-36.5px")
            //         .attr("xlink:href", function(d){ return d.img_hrefL});
            // }
            // })
            // .on("mouseout", function (d) { if(d.entity == "company")
            // {
            //     d3.select(this).attr("width", "70px")
            //         .attr("x", "-36px")
            //         .attr("y", "-36px")
            //         .attr("xlink:href", function(d){ return d.img_hrefD});
            // }
            // });


            //.text(function(d) { return d.name })
            node.append("svg:text")
            //****************************************
                .attr("class", function (d) {
                    return d.full_name
                })
                //****************************************
                .attr("x", 16)
                .attr("y", ".31em")
                //.attr("class", "shadow")
                //.style("font-size","10px")
                // .attr("dx", 0)
                // .attr("dy", ".35em")
                //.style("font-size","12px")
                //****************************************
                //text.shadow {
                .style("stroke", "#fff")
                .style("stroke-width", "4px")
                //}
                //.attr("class", "shadow")
                .style("font", String(fontSize) + "px Arial")
                //****************************************
                //.attr("text-anchor", "middle")
                //****************************************
                .text(function (d) {
                    return d.full_name
                });
            //****************************************


            //This one is for the actual text
            node.append("svg:text")
            //****************************************
                .attr("class", function (d) {
                    return d.full_name
                })
                //****************************************
                .attr("x", 16)
                .attr("y", ".31em")
                //.attr("class", "shadow")
                //.style("font-size","10px")
                // .attr("dx", 0)
                // .attr("dy", ".35em")
                //.style("font-size","12px")
                //****************************************
                .style("font", String(fontSize) + "px Arial")
                //****************************************
                //.attr("text-anchor", "middle")
                //****************************************
                .text(function (d) {
                    return d.full_name
                });
            //****************************************


            node.on("mouseover", function (d) {
                // d3.select(this).select("text")
                //     .transition()
                //     .duration(300)
                //     .text(function (d) {
                //         return d.full_name;
                //     })
                // //.style("font-size", "15px")
                // .style("font", "14px Times New Roman");
                //
                // d3.select(this).select("text")
                //     .transition()
                //     .duration(300)
                //     .text(function (d) {
                //         return d.full_name;
                //     })
                //     //.style("font-size", "15px")
                //     //.attr("class", "shadow")
                //     .style("font", "14px Times New Roman");
                // d3.select(this).select("text")
                //     .transition()
                //     .duration(300)
                //     .text(function (d) {
                //         return d.full_name;
                //     })
                //
                //     .style("fill",'black')
                //     .style("font", "14px Times New Roman");

                //d3.selectAll("text").remove();
                //d3.select(this).style("stroke-width", 6);

                //d3.select(this).select("text").style("stroke", "blue");

                var nodeNeighbors = links.filter(function (link) {
                    // Filter the list of links to only those links that have our target
                    // node as a source or target
                    return link.source.index === d.index || link.target.index === d.index;
                })
                    .map(function (link) {
                        // Map the list of links to a simple array of the neighboring indices - this is
                        // technically not required but makes the code below simpler because we can use
                        // indexOf instead of iterating and searching ourselves.
                        return link.source.index === d.index ? link.target.index : link.source.index;
                    });

                d3.selectAll('circle').filter(function (node) {
                    // I filter the selection of all circles to only those that hold a node with an
                    // index in my listg of neighbors
                    return nodeNeighbors.indexOf(node.index) > -1;
                })
                    .style('stroke', 'blue');

                //d3.selectAll('text').filter(d).style('fill', 'blue');
                //****************************
                // d3.selectAll('text').filter(function(node) {
                //     // I filter the selection of all circles to only those that hold a node with an
                //     // index in my listg of neighbors
                //     return nodeNeighbors.indexOf(node.index) > -1;
                // }).style('fill', 'blue')
                //     //.style("font-size", "16px")
                //     //.style("font-weight", "bold");
                // //****************************
                path.style('stroke', function (l) {
                    if (d === l.source || d === l.target)
                        return "blue";
                    else
                        return "grey";
                })

                path.style('stroke-width', function (l) {
                    if (d === l.source || d === l.target)
                        return 2;
                    else
                        return 1;
                })

            })
                .on("mouseout", function (d) {
                    d3.select(this).select("text")
                        .transition()
                        .duration(300)
                        .text(function (d) {

                            return d.full_name;
                        });
                    // d3.select(this).select("text")
                    //     //*******************************
                    //     .style("font", "14px Times New Roman")
                    //     //*******************************
                    //     .style("font-size", "14px")
                    //     .style("fill",'black')
                    //     .style("font-weight", "normal");

                    // d3.select(this).select("text")
                    // //*******************************
                    //     .style("font", "14px Times New Roman")
                    //     //*******************************
                    //     .style("font-size", "14px")
                    //     .style("fill",'black')
                    //     .style("font-weight", "normal");
                    //d3.select(this).style("stroke", "black");
                    //d3.select(this).style("stroke-width", 1);
                    //d3.select(this).style("stroke", "#333");
                    path.style('stroke', "grey");
                    path.style('stroke-width', 1);
                    //circle.style('stroke', "grey");
                    //node.style("stroke-width", 3);
                    //node.style("stroke", "#333");
                    //d3.selectAll('text').style('fill', 'black')
                    // d3.selectAll('text').style('fill', 'black')
                    //     .style("font-weight", "normal");
                    //d3.selectAll("text").style("font-weight", "normal");
                    node.selectAll("circle").style("stroke-width", 3)
                        .style('stroke', "black");
                    //.style("font-size", "12px");
                    //}
                });


            function pythag(r, b, coord) {
                r += nodeBaseRad;

                // force use of b coord that exists in circle to avoid sqrt(x<0)
                b = Math.min(w - r - strokeWidth, Math.max(r + strokeWidth, b));

                var b2 = Math.pow((b - radius), 2),
                    a = Math.sqrt(hyp2 - b2);

                function openLink() {
                    return function (d) {
                        var url = "";
                        if (d.slug != "") {
                            url = d.slug
                        } //else if(d.type == 2) {
                        //url = "clients/" + d.slug
                        //} else if(d.type == 3) {
                        //url = "agencies/" + d.slug
                        //}
                        window.open("//" + url)
                    }
                }

                // radius - sqrt(hyp^2 - b^2) < coord < sqrt(hyp^2 - b^2) + radius
                coord = Math.max(radius - a + r + strokeWidth,
                    Math.min(a + radius - r - strokeWidth, coord));

                return coord;
            }

            function tick(e) {
                path.attr("d", function (d) {
                    var dx = d.target.x - d.source.x,
                        dy = d.target.y - d.source.y,

                        dr = Math.sqrt(dx * dx + dy * dy);
                    ////console.log(d.source.x);
                    // //console.log(d.target.x);
                    return "M" + d.source.x + "," + d.source.y + "," + d.target.x + "," + d.target.y;
                    //return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
                });

                node.attr('x', function (d) {
                    return d.x = pythag(Math.random() * 12, d.y, d.x);
                })
                    .attr('y', function (d) {
                        return d.y = pythag(Math.random() * 12, d.x, d.y);
                    })
                    .attr("transform", function (d) {
                        return "translate(" + d.x + "," + d.y + ")"
                    });

                //d3.select(this).classed("fixed", d.fixed = true);
                // circle.attr("transform", function(d) {
                //     return "translate(" + d.x + "," + d.y + ")";
                // });
                //************************************
                // text.attr("transform", function(d) {
                //     return "translate(" + d.x + "," + d.y + ")";
                // });
                //************************************
            }

            //For not moving after drag
            var drag = force.drag()
                .on("dragstart", dragstart);
            //.on("dragstart", dragstartAll);

            //For not moving after drag
            function dblclick(d) {
                d3.select(this).classed("fixed", d.fixed = false);

            }

            //For not moving after drag
            function dragstart(d) {
                d3.select(this).classed("fixed", d.fixed = true);

                for (i = 0; i < nodes.length; i++) {
                    nodes[i].fixed = true;
                }
            }


            var svgText = svgGE.append("text");
            svgText.attr("x", 10).attr("y", globalHPlus50 - 50).text("PiNET-server @ www.pinet-server.org").style("font", "14px Times New Roman");

            //Added from here for coloring the legend
            if (1 == 0) {
                max_data = 1000;
                min_data = -1000;


                var colors = ["#00A6FF", "#1097E0", "#2885B7", "#35799E", "#4C7991", "#6D828D", "#8C8C8C", "#8E8E5C", "#92923C", "#A5A52E", "#BDBD24", "#DDDD15", "#FFFF00"];
                var domain_data = [-2.0, -1.6, -1.2, -0.8, -0.4, -0.01, 0.01, 0.4, 0.8, 1.2, 1.6, 2.0, 1000];


                var colorScale2 = d3.scale.threshold()
                    .domain(domain_data)
                    .range(colors);


                var legend2 = svgGE.selectAll(".legend")

                //.data([min_data, min_data + (max_data - min_data) / 7, min_data + 2 * (max_data - min_data) / 7, min_data + 3 * (max_data - min_data) / 7, min_data + 4 * (max_data - min_data) / 7, min_data + 5 * (max_data - min_data) / 7, min_data + 6 * (max_data - min_data) / 7], function (d) {
                    .data([-2.0, -1.6, -1.2, -0.8, -0.4, -0.01, 0.01, 0.4, 0.8, 1.2, 1.6, 2.0, 10.0], function (d) {

                        return d;
                    });

                // //console.log("colorScale.quantiles()");
                // //console.log(colorScale.quantiles());
                legend2.enter().append("g")
                    .attr("class", "legend");
                var gridSize = Math.floor(globalW / 40);
                var legendElementWidth = gridSize * 2;
                legend2.append("rect")
                    .attr("x", function (d, i) {
                        return legendElementWidth * i;
                    })
                    .attr("y", globalHPlus50 - 40)
                    .attr("width", legendElementWidth)
                    .attr("height", gridSize / 2)
                    .style("fill", function (d, i) {
                        return colors[i];
                    });

                legend2.append("text")
                //.attr("class", "mono")
                    .text(function (d, i) {
                        if (i == 0) {
                            return " a < " + parseFloat(Math.round(d * 100) / 100).toFixed(1);
                        }
                        else if (i == svgGE.selectAll(".legend").data().length - 1) {

                            return parseFloat(Math.round((svgGE.selectAll(".legend").data()[i - 1]) * 100) / 100).toFixed(1) + " ≤ a ";
                        }
                        else {

                            return parseFloat(Math.round((svgGE.selectAll(".legend").data()[i - 1]) * 100) / 100).toFixed(1) + " ≤ a < " + parseFloat(Math.round(d * 100) / 100).toFixed(1);
                        }
                        //return  parseFloat(Math.round(d * 100) / 100).toFixed(2) + "≥ a";
                    })
                    .style("font", "11px Times New Roman")
                    .attr("x", function (d, i) {
                        return legendElementWidth * i;
                    })
                    .attr("y", globalHPlus50 - 40 + gridSize);

                legend2.exit().remove();
            }

            //legend2.exit().remove();

            //till here for coloring the legend


            // For legend
            // var colNodeScaleSeparateInfo = d3.scale.ordinal()
            //     .range(["#767776", "#f91104"])
            //     .domain(["Query Gene Set", "Pathways / Kinases Perturbation"]);
            //
            //
            // var legend = svg.selectAll(".legend")
            //     .data(colNodeScaleSeparateInfo.domain())
            //     .enter().append("g")
            //     .attr("class", "legend")
            //     .attr("transform", function (d, i) {
            //         return "translate(0," + (i) * 25 + ")";
            //     });
            //
            // legend.append("rect")
            //     .attr("x", w - 25)
            //     .attr("width", 25)
            //     .attr("height", 25)
            //     .style("fill", colNodeScaleSeparateInfo);
            //
            // legend.append("text")
            //     .attr("x", w - 35)
            //     .attr("y", 12.5)
            //     .attr("dy", ".35em")
            //     .style("text-anchor", "end")
            //     .text(function (d) {
            //         return d;
            //     });
            //
            //
            // d3.select("#download").on("click", function () {
            //     d3.select(this)
            //         .attr("href", 'data:application/octet-stream;base64,' + btoa(d3.select("#chart").html()))
            //         .attr("download", "pathway_network.svg")
            // })

        };

        //defaultSVGPtm();
        //SharedService.setVar('svg', svg);

        d3.select('#forceGE').on('click', function () {
            defaultSVGGE();
            self.graphType = 3;

        });

        if (graphType == 0) {
            circosViewGE();
        } else if (graphType == 1) {
            circularViewGE();
        } else if (graphType == 2) {
            parallelViewGE();
        } else if (graphType == 3) {
            defaultSVGGE();
        }


        // d3.select("#GE").on("click", function() {
        //     d3.select(this)
        //         .attr("href", 'data:application/octet-stream;base64,' + btoa(d3.select("#line").html()))
        //         .attr("download", "viz.svg")
        // })
        d3.select("#download-svgGE").on("click", function () {
            var name = fileName.concat('.svg');
            var svgEl = svgGE.node();
            svgEl.setAttribute("xmlns", "http://www.w3.org/2000/svg");
            var svgData = svgEl.outerHTML;
            var preface = '<?xml version="1.0" standalone="no"?>\r\n';
            var svgBlob = new Blob([preface, svgData], {type: "image/svg+xml;charset=utf-8"});
            var svgUrl = URL.createObjectURL(svgBlob);
            var downloadLink = document.createElement("a");
            downloadLink.href = svgUrl;
            downloadLink.download = name;
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
        })

        // d3.select("#download-svgGE").on("click", function () {
        //     console.log("#download-svgGE")
        //     d3.select(this)
        //         .attr("href", 'data:application/octet-stream;base64,' + btoa(d3.select("#chartGE")))
        //         .attr("download", "pathway_network.svg")
        // })

        d3.select('#download-pngGE').on('click', function () {
            var svgString = getSVGString(svgGE.node());


            svgString2Image(svgString, 4 * globalW, 4 * globalHPlus50, 'png', save); // passes Blob and filesize String to the callback

            function save(dataBlob, filesize) {
                saveAs(dataBlob, fileName.concat('.png')); // FileSaver.js function
            }
        });
        d3.select('#saveButton').on('click', function () {
            var svgString = getSVGString(svg4.node());

            svgString2Image(svgString, 4 * globalW, 4 * globalHPlus50, 'png', save); // passes Blob and filesize String to the callback

            function save(dataBlob, filesize) {
                saveAs(dataBlob, fileName.concat('.png')); // FileSaver.js function
            }
        });

// Below are the functions that handle actual exporting:
// getSVGString ( svgNode ) and svgString2Image( svgString, width, height, format, callback )
        function getSVGString(svgNode) {
            svgNode.setAttribute('xlink', 'http://www.w3.org/1999/xlink');
            var cssStyleText = getCSSStyles(svgNode);
            appendCSS(cssStyleText, svgNode);

            var serializer = new XMLSerializer();
            var svgString = serializer.serializeToString(svgNode);
            svgString = svgString.replace(/(\w+)?:?xlink=/g, 'xmlns:xlink='); // Fix root xlink without namespace
            svgString = svgString.replace(/NS\d+:href/g, 'xlink:href'); // Safari NS namespace fix

            return svgString;

            function getCSSStyles(parentElement) {
                var selectorTextArr = [];

                // Add Parent element Id and Classes to the list
                selectorTextArr.push('#' + parentElement.id);
                for (var c = 0; c < parentElement.classList.length; c++)
                    if (!contains('.' + parentElement.classList[c], selectorTextArr))
                        selectorTextArr.push('.' + parentElement.classList[c]);

                // Add Children element Ids and Classes to the list
                var nodes = parentElement.getElementsByTagName("*");
                for (var i = 0; i < nodes.length; i++) {
                    var id = nodes[i].id;
                    if (!contains('#' + id, selectorTextArr))
                        selectorTextArr.push('#' + id);

                    var classes = nodes[i].classList;
                    for (var c = 0; c < classes.length; c++)
                        if (!contains('.' + classes[c], selectorTextArr))
                            selectorTextArr.push('.' + classes[c]);
                }

                // Extract CSS Rules
                var extractedCSSText = "";
                for (var i = 0; i < document.styleSheets.length; i++) {
                    var s = document.styleSheets[i];

                    try {
                        if (!s.cssRules) continue;
                    } catch (e) {
                        if (e.name !== 'SecurityError') throw e; // for Firefox
                        continue;
                    }

                    var cssRules = s.cssRules;
                    for (var r = 0; r < cssRules.length; r++) {
                        if (contains(cssRules[r].selectorText, selectorTextArr))
                            extractedCSSText += cssRules[r].cssText;
                    }
                }


                return extractedCSSText;

                function contains(str, arr) {
                    return arr.indexOf(str) === -1 ? false : true;
                }

            }

            function appendCSS(cssText, element) {
                var styleElement = document.createElement("style");
                styleElement.setAttribute("type", "text/css");
                styleElement.innerHTML = cssText;
                var refNode = element.hasChildNodes() ? element.children[0] : null;
                element.insertBefore(styleElement, refNode);
            }
        }


        function svgString2Image(svgString, width, height, format, callback) {
            var format = format ? format : 'png';

            var imgsrc = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgString))); // Convert SVG string to data URL

            var canvas = document.createElement("canvas");
            var context = canvas.getContext("2d");

            canvas.width = width;
            canvas.height = height;

            var image = new Image();
            image.onload = function () {
                context.clearRect(0, 0, width, height);
                context.drawImage(image, 0, 0, width, height);

                canvas.toBlob(function (blob) {
                    var filesize = Math.round(blob.length / 1024) + ' KB';
                    if (callback) callback(blob, filesize);
                });


            };

            image.src = imgsrc;
        }


        self.showGEGraph = true;
        self.showGEGraph = true;


    }


// //console.log(network.parallel);
// //console.log(network.circular);
// update(network.nodes, network.edges, network.parallel, network.circular);
//console.log(network.nodes);
//console.log(ptmToAbundance);
    for (var iterNetNode = 0; iterNetNode < input_network.nodes.length; iterNetNode++) {
        var iterNetNodeKey = input_network.nodes[iterNetNode]["name"];
        if (iterNetNodeKey in ptmToAbundance) {
            //console.log(iterNetNodeKey);
            if (ptmToAbundance[iterNetNodeKey] == "NA") {
                input_network.nodes[iterNetNode]["value"] = 0.0;
            }
            else {
                input_network.nodes[iterNetNode]["value"] = ptmToAbundance[iterNetNodeKey];
            }
        }
    }
//console.log(self.computeWeightForupdatePtm);
// if(self.computeWeightForUpdateGE) {
//console.log("---  inside computeWeightForUpdatePtm");
    for (var iterNetNode = 0; iterNetNode < input_network.edges.length; iterNetNode++) {
        //var iterNetNodeKey = network.nodes[iterNetNode]["name"];
        var idx1 = input_network.edges[iterNetNode]["source"];
        var idx2 = input_network.edges[iterNetNode]["target"];
        console.log(idx1);
        console.log(idx2);


        if (typeof idx1 == 'object') {
            idx1 = idx1["idx"];
            input_network.nodes[idx1]["weight"] += 1;

        }
        if (typeof idx1 == 'object') {
            idx2 = idx2["idx"];
            input_network.nodes[idx2]["weight"] += 1;
        }
        console.log(input_network);


    }
    self.computeWeightForUpdateGE = false;

//console.log(network);
    updateGE(input_network.nodes, input_network.edges, fontSize, widthSize, circleSize, nodeSize);
    console.log("self.showGEGraph");
    console.log(self.showGEGraph);


    self.showGEGraph = true;
}


function convertToCSV(objArray) {
    var array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;
    var str = '';

    for (var i = 0; i < array.length; i++) {
        var line = '';
        for (var index in array[i]) {
            if (line != '') line += ','

            line += array[i][index];
        }

        str += line + '\r\n';
    }

    return str;
}

