$(document).ready(function() {
  var socket;

  // Websocket connection opened
  socket = new ReconnectingWebSocket("wss://91b7nuay0h.execute-api.us-east-1.amazonaws.com/dev");

  socket.onopen = function(event) {
    console.log("Socket is open!");
    // API Key associated with the connection
    data = {"action": "add_api_key", "api_key" : "api_key"};
    socket.send(JSON.stringify(data));
  };

  // Setup listener for messages
  socket.onmessage = function(message) {
    var data = JSON.parse(message.data);

    if (data.event_type == "hover") {
      drawDashboard(data, "hovers");
    } else if (data.event_type == "click") {
      drawDashboard(data, "clicks");
    }
  };
});
