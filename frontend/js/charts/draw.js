function drawChart(data, dashboard_type) {
  var colors = [];
  var colors_and_counts = {};
  var html_id = ""; // id of the div where the chart will be rendered

  if (dashboard_type == "clicks") {
    html_id = "#clicks_dashboard";
    chart_title = "Clicks";
  } else if (dashboard_type == "hovers") {
    html_id = "#hovers_dashboard";
    chart_title = "Hovers";
  }

  $.each( data.stats, function( key, val ) {
    colors.push(val.color);
    colors_and_counts[val.color] = parseInt(val.count);
  });

  // set the dimensions and margins of the graph
  var width = 350
      height = 350
      margin = 40

  // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
  var radius = Math.min(width, height) / 2 - margin

  // remove old graph to allow new graph to be rendered
  $(html_id).html("");

  // append the svg object to the div called 'html_id'
  var svg = d3.select(html_id)
    .append("svg")
      .attr("width", width)
      .attr("height", height)
    .append("g")
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

  var data = {
    a: colors_and_counts["green"],
    b: colors_and_counts["red"],
    c: colors_and_counts["blue"],
    d: colors_and_counts["yellow"]
  }

  // set the color scale
  var color = d3.scaleOrdinal()
    .domain(data)
    .range(colors)

  // Compute the position of each group on the pie:
  var pie = d3.pie()
    .value(function(d) {return d.value; })
  var data_ready = pie(d3.entries(data))

  // shape helper to build arcs:
  var arcGenerator = d3.arc()
    .innerRadius(50)
    .outerRadius(radius)

  // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
  svg
    .selectAll("whatever")
    .data(data_ready)
    .enter()
    .append("path")
    .attr("d", d3.arc()
      .innerRadius(50)         // This is the size of the donut hole
      .outerRadius(radius)
    )
    .attr("fill", function(d){ return(color(d.data.key)) })
    .attr("stroke", "grey")
    .style("stroke-width", "5px")
    .style("opacity", 0.7)

  // Adding numbers inside each piece of the pie chart
  svg
    .selectAll("whatever")
    .data(data_ready)
    .enter()
    .append("text")
    .text(function(d){ return d.data.value })
    .attr("transform", function(d) { return "translate(" + arcGenerator.centroid(d) + ")";  })
    .style("text-anchor", "middle")
    .style("font-size", 30)

  // Adding "Clicks/Hovers" title inside pie chart
  svg.append("text")
     .attr("text-anchor", "middle")
     .style("font-size", 25)
     .text(chart_title);
};
