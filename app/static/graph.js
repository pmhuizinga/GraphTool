function create_graph(base, id) {
    console.log('base: ' + base + '. id: ' + id)
    d3.select('svg').selectAll("*").remove();

    var svg = d3.select("svg"),
        width = +svg.attr("width"),
        height = +svg.attr("height");

    var color = d3.scaleOrdinal(d3.schemeCategory10);

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function (d) {
            return d.id;
        }))
        .force("charge", d3.forceManyBody().strength(-80))
        .force("center", d3.forceCenter(width / 2, height / 2));

    d3.json('/graph_nodes/' + base + '/' + id, function (error, nodes) {
        // remove alias nodes
        nodes = nodes.filter(function(d) { return d.node_type != 'alias'})
        d3.json('/graph_edges/' + base + '/' + id, function (error, links) {
            // remove alias links
            links = links.filter(function(d) { return d.edge_type != 'has_alias'})

            // LEGEND
            // get unique list of nodes
            node_types = d3.set(nodes.map(d => d.node_type)).values()

            // console.log(node_types)
            const legend = svg.append("g")
                .attr("transform", `translate(${50}, ${10})`)

            node_types.forEach((node_id, i) => {

                const legendRow = legend.append("g")
                    .attr("transform", `translate(0, ${i * 20})`)

                legendRow.append("circle")
                    .attr("class", "nodes")
                    .attr("r", 7)
                    .attr("fill", color(node_id))
                    .attr("stroke", "white")
                    .attr("stroke-width", "1.5px")
                    .on('mousedown', function() { console.log('mousedown on legend item: ' + node_id); } );

                legendRow.append("text")
                    .attr("x", 10)
                    .attr("y", 5)
                    .attr("text-anchor", "start")
                    .text(node_id)
            })

            // END LEGEND
            // NODE INFO
            const node_info = svg.append("g")
                .attr("transform", `translate(${width - 150}, ${10})`)
            // END NODE INFO

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
                .enter()
                    .append("line")
                .filter(function(d) {return d.node_type != 'has_alias'})
                .attr("stroke-width", 2)
                .on('mousedown', function() { console.log('mousedown on link item: not defined') } )
                // .selectAll("text")
                // .data(links)
                // .enter()
                // .append("text")
                // .text(function(d) {return 'test'})
                ;

            var node = svg.append("g")
                .attr("class", "nodes")
                .selectAll("g")
                .data(nodes)
                .enter().append("g")
                .on('mouseover', function(d) {
                    node_info.selectAll("*").remove()
                    // node_info.append("text")
                    //     .attr("x", 0)
                    //     .attr("y", 0)
                    //     .attr("text-anchor", "start")
                    //     .text('node type: ' + d.node_type)
                    // node_info.append("text")
                    //     .attr("x", 0)
                    //     .attr("y", 20)
                    //     .attr("text-anchor", "start")
                    //     .text('node id: ' + d.node_id)

                    // node_info.forEach((node_id, i) => {
                    // data.forEach((node_attr, i) => {
                    // nodes.forEach(d.node_attr.replaceAll("'",'"'), function( k, v ) {
                    //     console.log( "Key: " + k + ", Value: " + v );
                    // })

                    // node_info.append("text")
                    //     .attr("x", 0)
                    //     .attr("y", 40)
                    //     .attr("text-anchor", "start")
                    //     .text('node attr: ' + d.node_attr)

                    // let a = d.node_attr.replaceAll("'",'"')
                    // console.log('a: ' + a)
                    // console.log('typof a: ' + typeof a)
                    // let b = JSON.parse(a)
                    // console.log('b: ' + b)
                    // console.log('typeof b: ' + typeof b)
                    // b.forEach(content, function(k,v)
                    //     {
                    //         console.log('key: ' + k + ',value: ' + v)
                    //     }
                    // )
                    const text = JSON.parse(d.node_attr.replaceAll("'",'"'));
                    console.log(text)
                    let j = 0
                    for (const key in text) {

                         const node_info_row = node_info.append("g")
                            .attr("transform", `translate(0, ${j})`)

                        // node_info_row.append("circle")
                        //     .attr("class", "nodes")
                        //     .attr("r", 7)
                        //     .attr("fill", color(node_id))
                        //     .attr("stroke", "white")
                        //     .attr("stroke-width", "1.5px")
                        //     .on('mousedown', function() { console.log('mousedown on legend item: ' + node_id); } );

                        node_info_row.append("text")
                            .attr("x", 0)
                            .attr("y", 0)
                            .attr("text-anchor", "start")
                            .text(`${key}: ${text[key]}`)

                        j += 20
                        console.log(j)
                        console.log(`${key}: ${text[key]}`);
                    }

                    // Object.keys(text).forEach(function(k,v){
                    //   console.log(k,v)
                    // });

                    // Object.keys(text).forEach(function(key, value) {
                    //    console.log(key, value);
                    // });
                    // text.keys().forEach(function(key) {
                    //    console.log(key + " " + obj[key]);
                    // });
                    // text.forEach((k, v) => console.log(`Key is ${k} and value is ${v}`));
                    // console.log(text)
                    // const obj = JSON.parse(text, function (key, value) {
                    //     console.log(key, value)
                    // });
                    // console.log(d.node_attr.replaceAll("'",'"'))
                    // node_info.append("text")
                    //     .attr("x", 0)
                    //     .attr("y", 60)
                    //     .attr("text-anchor", "start")
                    //     .text('node attr: ' + JSON.parse('{"key":"value"}'))
                })
                .on('mouseout', function(d) {
                    node_info.selectAll("*").remove()
                })
                // .filter(function(d) {return d.node_type != 'alias'})

            function write_node_info()
                {

                }


            var circles = node.append("circle")
                .attr("r", 9)
                .attr("fill", function (d) {
                    return color(d.node_type);
                })
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));

            //onderstaand zorgt voor de node titles
            var labels = node.append("text")
                .text(function (d) {
                    return d.node_id;
                })
                .attr('x', 10)
                .attr('y', 3);

            // var link_l = link.append("path")
            //     .attr("class", "link")

            var link_labels = link.append("text")
                .attr("dy", ".35em")
                .attr("text-anchor", "middle")
                .attr('x', 3)
                .attr('y', 3)
                .text(function (d) {
                    // console.log(d.type)
                    return d.type;
                })

            // var linktext = svg.selectAll("g.linklabelholder").data(links);
            //     linktext.enter().append("g").attr("class", "linklabelholder")
            //     .append("text")
            //     .attr("class", "linklabel")
            //     // .attr("dx", 1)
            //     .attr("dy", ".35em")
            //     .text(function(d) { return "my label" });

            // link.append("title")
            //     .text(function(d) {
            //             console.log(d.type)
            //              return d.type
            //         });

            // link.append("text")
            //     .attr("font-family", "Arial, Helvetica, sans-serif")
            //     .attr("fill", "Black")
            //     .style("font", "normal 12px Arial")
            //     .attr("dy", ".35em")
            //     .attr("text-anchor", "middle")
            //     // .attr('x', 10)
            //     // .attr('y', 3)
            //     .text(function(d) {
            //         console.log(d.type)
            //          return d.type
            //     });

            // link.append("title")
            //     .text(function (d) {
            //         // return d.edge_type;
            //         return "test";
            //     });

            // node.append("title")
            //     .text(function (d) {
            //         return d.node_id;
            //     });

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
        create_graph('node', d.name)
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

     function clicklegend(d) {
        console.log('click legend')
    }
    ;
}