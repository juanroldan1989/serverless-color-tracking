$(document).ready(function() {
  var socket;

  // Connect websockets
  socket = new ReconnectingWebSocket("wss://s1h9o8dplb.execute-api.us-east-1.amazonaws.com/dev");

  socket.onopen = function(event) {
    console.log("Socket is open!");
    data = {"action": "live", "api_key" : "api_key", "event_type": "click"};
    socket.send(JSON.stringify(data));
  };

  // Setup listener for messages
  socket.onmessage = function(message) {
    var data = JSON.parse(message.data);
    console.log(data);
  };
});
