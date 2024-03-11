$(document).ready(function() {
  var socket;

  // Connect websockets
  socket = new ReconnectingWebSocket("wss://s1h9o8dplb.execute-api.us-east-1.amazonaws.com/dev");

  socket.onopen = function(event) {
    console.log("Socket is open!");
    // connection oppened and `Connection` record added to DynamoDB
  };

  // Setup listener for messages via websockets
  socket.onmessage = function(message) {
    var data = JSON.parse(message.data);
    console.log(data);

    if (data.event_type == "hover") {
      drawDashboard(data, "hovers");
    } else if (data.event_type == "click") {
      drawDashboard(data, "clicks");
    }
  };
});
