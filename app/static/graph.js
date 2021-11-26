function create_graph(base, id) {
    // console.log('base: ' + base)
    d3.select('svg').selectAll("*").remove();

    var svg = d3.select("svg"),
        width = +svg.attr("width"),
        height = +svg.attr("height");

    var color = d3.scaleOrdinal(d3.schemeCategory10);

    // var node_type = d3.scaleOrdinal();

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function (d) {
            return d.id;
        }))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    d3.json('/graph_nodes/' + base + '/' + id, function (error, nodes) {
        // remove alias nodes
        nodes = nodes.filter(function(d) { return d.type != 'alias'})
        d3.json('/graph_edges/' + base + '/' + id, function (error, links) {
            // remove alias links
            links = links.filter(function(d) { return d.type != 'has_alias'})

            // LEGEND
            // get unique list of nodes
            node_names = d3.set(nodes.map(d => d.type)).values()

            console.log(node_names)

            const legend = svg.append("g")
                .attr("transform", `translate(${50}, ${10})`)

            node_names.forEach((name, i) => {

                const legendRow = legend.append("g")
                    .attr("transform", `translate(0, ${i * 20})`)

                legendRow.append("circle")
                    .attr("class", "nodes")
                    .attr("r", 7)
                    .attr("fill", color(name))
                    .attr("stroke", "white")
                    .attr("stroke-width", "1.5px")

                legendRow.append("text")
                    .attr("x", 10)
                    .attr("y", 5)
                    .attr("text-anchor", "start")
                    .text(name)
            })

            // END LEGEND
            if (error) throw error;
            console.log('nodes')
            console.log(nodes)
            console.log('links')
            console.log(links)

            // Add lines for every link in the dataset
            var link = svg.append("g")
                .attr("class", "links")
                .selectAll("line")
                .data(links)
                .enter().append("line")
                // .attr("stroke-width", function(d) { return Math.sqrt(d.value); });
                .filter(function(d) {return d.type != 'has_alias'})
                .attr("stroke-width", 2);

            var node = svg.append("g")
                .attr("class", "nodes")
                .selectAll("g")
                .data(nodes)
                .enter().append("g")
                // .filter(function(d) {return d.type != 'alias'})

            var circles = node.append("circle")
                .attr("r", 9)
                .attr("fill", function (d) {
                    return color(d.type);
                })
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));

            var labels = node.append("text")
                .text(function (d) {
                    return d.id;
                })
                .attr('x', 10)
                .attr('y', 3);

            node.append("title")
                .text(function (d) {
                    return d.id;
                });

            simulation
                .nodes(nodes)
                .on("tick", ticked);

            simulation.force("link")
                .links(links);

            function ticked() {
                link
                    .attr("x1", function (d) {
                        return d.source.x;
                    })
                    .attr("y1", function (d) {
                        return d.source.y;
                    })
                    .attr("x2", function (d) {
                        return d.target.x;
                    })
                    .attr("y2", function (d) {
                        return d.target.y;
                    });

                node
                    .attr("transform", function (d) {
                        return "translate(" + d.x + "," + d.y + ")";
                    })
            }
        })
    });

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.7).restart();
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
}