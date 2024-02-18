const data = [
    { name: "Donor1", party: "Party A", amount: 200, year: 2012 },
    { name: "Donor2", party: "Party B", amount: 500, year: 2014 },
    { name: "Donor3", party: "Party A", amount: 300, year: 2016 },
    // Add more rows according to the pattern
];


// Dimensions and margins
const margin = {top: 20, right: 20, bottom: 50, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// Append the svg object to the body of the page
const svg = d3.select("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// A color scale for parties
const color = d3.scaleOrdinal()
    .domain(data.map(d => d.party))
    .range(d3.schemeCategory10);

// A scale for bubble sizes
const size = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.amount)])
    .range([5, 40]); // Bubble radius

// X scale for years
const x = d3.scaleLinear()
    .domain(d3.extent(data, d => d.year))
    .range([0, width]);

// Add a scale for bubble placement
const y = d3.scaleOrdinal()
    .domain([...new Set(data.map(d => d.party))])
    .range([height, 0]);

// Add circles
svg.selectAll("circle")
    .data(data)
    .join("circle")
    .attr("cx", d => x(d.year))
    .attr("cy", d => y(d.party))
    .attr("r", d => size(d.amount))
    .style("fill", d => color(d.party))
    .attr("stroke", "black");

// Add year axis
svg.append("g")
    .attr("transform", `translate(0,${height + 10})`)
    .call(d3.axisBottom(x).tickFormat(d3.format("d")));

// Add party axis (optional, for clarity)
svg.append("g")
    .call(d3.axisLeft(y));

