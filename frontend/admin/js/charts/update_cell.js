function updateCell(api_key, action, color, count) {
  var cell_id = "#" + api_key + "_" + action + "_" + color;

  console.log("cell_id: ", cell_id);

  if ($(cell_id).length) {
    $(cell_id).text(count);
  } else {
    console.log("cell_id not found: ", cell_id);
    console.log("creating row for: ", cell_id);

    var new_row = "<tr>"; // api_key, action, count
    new_row += "<td>" + api_key + "</td>";
    new_row += "<td>" + action + "</td>";
    new_row += `<td style='background-color: ${color} !important' id='` + api_key + "_" + action + "_" + color + "'>" + count + "</td>";
    new_row += "</tr>";

    console.log("new_row: ", new_row);
    var table_body = $("#stats tbody");
    $(table_body).append(new_row);
  }
};
