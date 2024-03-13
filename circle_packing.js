d3.json('data/circlePackingData.json').then(data => {
    // Setup dimensions and margins for the visualization
    const width = 600, height = 600;
    
    // Create the SVG container for the visualization and append it to #circlePacking div
    const svg = d3.select('#circlePacking').append('svg')
        .attr('width', width)
        .attr('height', height);

    // Define a color scale (optional)
    const color = d3.scaleLinear()
        .domain([0, 5])  // Depth level
        .range(["hsl(152,80%,80%)", "hsl(228,30%,40%)"])
        .interpolate(d3.interpolateHcl);

    // Create a layout for circle packing
    const pack = d3.pack()
        .size([width - 2, height - 2])
        .padding(3);

    const root = d3.hierarchy(data)
        .sum(d => d.value)
        .sort((a, b) => b.value - a.value);

    // Apply the layout to the data
    pack(root);

    // Draw circles
    const node = svg.selectAll('g')
        .data(root.descendants())
        .enter().append('g')
        .attr('transform', d => `translate(${d.x},${d.y})`);

    node.append('circle')
        .attr('r', d => d.r)
        .style('fill', d => color(d.depth));
        
    // Optionally, add labels or other visual elements here
});