// Include D3.js via a script tag in your HTML or import it if using a module bundler

// Define the main function to draw the treemap
function drawTreemap() {
  // Load and parse the CSV data
  d3.csv('assets/bond_details.csv', {
      delimiter: ';'
  }).then(data => {
      // Convert 'denomination' to numbers
      data.forEach(d => {
          d.denomination = +d.denomination;
      });

      // Aggregate data by 'name_of_purchaser'
      let aggregatedData = d3.rollup(data, v => d3.sum(v, d => d.denomination), d => d.name_of_purchaser);

      // Convert the aggregated data into a hierarchy
      let root = {
          name: "root",
          children: Array.from(aggregatedData, ([name, value]) => ({name, value}))
      };

      // Setup dimensions and margins for the visualization
      const width = 960, height = 600;

      // Create the SVG container and append it to body or specific div
      const svg = d3.select('body').append('svg')
          .attr('width', width)
          .attr('height', height)
          .style('font', '10px sans-serif');

      // Define a treemap layout
      const treemap = d3.treemap()
          .size([width, height])
          .padding(1);

      // Process the hierarchical data
      let hierarchy = d3.hierarchy(root)
          .sum(d => d.value) // Here the value is the aggregated 'denomination'
          .sort((a, b) => b.height - a.height || b.value - a.value);

      treemap(hierarchy);

      // Drawing the treemap
      const cell = svg.selectAll("g")
          .data(hierarchy.leaves())
          .enter().append("g")
          .attr("transform", d => `translate(${d.x0},${d.y0})`);

      cell.append("rect")
          .attr("id", d => (d.leafUid = DOM.uid("leaf")).id)
          .attr("width", d => d.x1 - d.x0)
          .attr("height", d => d.y1 - d.y0)
          .attr("fill", d => {
              while (d.depth > 1) d = d.parent;
              return d3.scaleOrdinal(d3.schemeCategory10)(d.data.name);
          });

      cell.append("clipPath")
          .attr("id", d => (d.clipUid = DOM.uid("clip")).id)
          .append("use")
          .attr("xlink:href", d => d.leafUid.href);

      cell.append("text")
          .attr("clip-path", d => d.clipUid)
          .selectAll("tspan")
          .data(d => d.data.name.split(/(?=[A-Z][^A-Z])/g))
          .join("tspan")
          .attr("x", 3)
          .attr("y", (d, i, nodes) => `${1.1 + i * 0.9}em`)
          .text(d => d);

      // Add other elements like title, interactivity as required
  }).catch(error => {
      console.error("Error loading or processing data:", error);
  });
}

// Call the main function to draw the treemap
drawTreemap();