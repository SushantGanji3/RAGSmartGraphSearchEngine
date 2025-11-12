import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const KnowledgeGraph = ({ results }) => {
  const svgRef = useRef();

  useEffect(() => {
    if (!results || results.length === 0) return;

    // Clear previous graph
    d3.select(svgRef.current).selectAll("*").remove();

    const width = 800;
    const height = 600;
    const svg = d3.select(svgRef.current)
      .attr("width", width)
      .attr("height", height);

    // Create nodes from results
    const nodes = results.map((result, i) => ({
      id: result.id,
      title: result.title,
      group: i,
      x: Math.random() * width,
      y: Math.random() * height,
    }));

    // Create links (simplified - connect first result to others)
    const links = [];
    if (nodes.length > 1) {
      for (let i = 1; i < nodes.length; i++) {
        links.push({
          source: nodes[0].id,
          target: nodes[i].id,
        });
      }
    }

    // Create force simulation
    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id).distance(100))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2));

    // Draw links
    const link = svg.append("g")
      .selectAll("line")
      .data(links)
      .enter().append("line")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .attr("stroke-width", 2);

    // Draw nodes
    const node = svg.append("g")
      .selectAll("circle")
      .data(nodes)
      .enter().append("circle")
      .attr("r", 20)
      .attr("fill", (d, i) => d3.schemeCategory10[i % 10])
      .call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended));

    // Add labels
    const label = svg.append("g")
      .selectAll("text")
      .data(nodes)
      .enter().append("text")
      .text(d => d.title.length > 20 ? d.title.substring(0, 20) + "..." : d.title)
      .attr("font-size", "12px")
      .attr("dx", 25)
      .attr("dy", 5)
      .attr("fill", "#333");

    // Update positions on tick
    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);

      label
        .attr("x", d => d.x)
        .attr("y", d => d.y);
    });

    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    return () => {
      simulation.stop();
    };
  }, [results]);

  if (!results || results.length === 0) {
    return null;
  }

  return (
    <div className="w-full max-w-4xl mx-auto mt-8">
      <h2 className="text-2xl font-bold mb-4">Knowledge Graph</h2>
      <div className="bg-white rounded-lg shadow-md p-4 overflow-auto">
        <svg ref={svgRef} className="w-full"></svg>
      </div>
    </div>
  );
};

export default KnowledgeGraph;

