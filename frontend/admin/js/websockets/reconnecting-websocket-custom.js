$(document).ready(function() {
  var socket;

  // Websocket connection opened
  socket = new ReconnectingWebSocket("wss://91b7nuay0h.execute-api.us-east-1.amazonaws.com/dev");

  socket.onopen = function(event) {
    console.log("Socket is open!");
    // API Key associated with the connection
    data = {"action": "add_api_key", "api_key" : "admin_api_key"};
    socket.send(JSON.stringify(data));
  };

  // Setup listener for messages
  socket.onmessage = function(message) {
    var data = JSON.parse(message.data);

    // data = {
    //   "api_key" : "api_key",
    //   "action" : "hover",
    //   "color" : "blue",
    //   "count" : 317
    // }

    if (data.api_key && data.action && data.color && data.count) {
      updateCell(data.api_key, data.action, data.color, data.count);
    }
  };
});
