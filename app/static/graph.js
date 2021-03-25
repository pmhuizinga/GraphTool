// data = {
//   "nodes": [
//     {"id": "Myriel", "group": 1},
//     {"id": "Napoleon", "group": 1},
//     {"id": "Mlle.Baptistine", "group": 1}
//   ],
//   "links": [
//     {"source": "Napoleon", "target": "Myriel", "value": 1},
//     {"source": "Mlle.Baptistine", "target": "Myriel", "value": 8}
//   ]
// }
//
// nodes =  [
//     {"id": "Myriel", "group": 1},
//     {"id": "Napoleon", "group": 2},
//     {"id": "Mlle.Baptistine", "group": 1}
//     ]
//
// links = [
//     {"source": "Napoleon", "target": "Myriel", "value": 8},
//     {"source": "Mlle.Baptistine", "target": "Myriel", "value": 8}
//   ]


var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var color = d3.scaleOrdinal(d3.schemeCategory20);

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2));


d3.json('/graph_nodes',function(error, nodes){
    d3.json('/graph_edges',function(error, links){

   if (error) throw error;

    // Add lines for every link in the dataset
    var link = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(links)
        .enter().append("line")
            // .attr("stroke-width", function(d) { return Math.sqrt(d.value); });
            .attr("stroke-width", 2);

  var node = svg.append("g")
      .attr("class", "nodes")
      .selectAll("g")
      .data(nodes)
      .enter().append("g")

  var circles = node.append("circle")
      .attr("r", 7)
      .attr("fill", function(d) { return color(d.group); })
      .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

  var lables = node.append("text")
      .text(function(d) {
        return d.id;
      })
      .attr('x', 6)
      .attr('y', 3);

  node.append("title")
      .text(function(d) { return d.id; });

  simulation
      .nodes(nodes)
      .on("tick", ticked);

  simulation.force("link")
      .links(links);

  function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("transform", function(d) {
          return "translate(" + d.x + "," + d.y + ")";
        })
  }
})});

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
};