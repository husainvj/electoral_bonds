d3.csv('data/areaChartData.csv').then(data => {
    // Setup dimensions and scales
    const margin = {top: 20, right: 20, bottom: 30, left: 50},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    const x = d3.scaleTime().range([0, width]),
        y = d3.scaleLinear().range([height, 0]),
        z = d3.scaleOrdinal(d3.schemeCategory10);

    // Define the stack generator
    const stack = d3.stack();

    // Create SVG
    const svg = d3.select("#stackedAreaChart").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Process data
    const keys = data.columns.slice(1);
    const series = stack.keys(keys)(data);

    x.domain(d3.extent(data, d => d.date));
    z.domain(keys);

    // Add areas
    svg.selectAll(".layer")
      .data(series)
      .enter().append("path")
        .attr("class", "layer")
        .attr("d", d3.area()
            .x(d => x(d.data.date))
            .y0(d => y(d[0]))
            .y1(d => y(d[1]))
        )
        .attr("fill", d => z(d.key));

    // Add axes and other necessary elements
});