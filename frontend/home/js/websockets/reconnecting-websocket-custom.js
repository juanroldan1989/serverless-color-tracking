$(document).ready(function() {
  var socket;

  // Connect websockets
  socket = new ReconnectingWebSocket("wss://i9wbghqbpf.execute-api.us-east-1.amazonaws.com/dev");

  socket.onopen = function(event) {
    console.log("Socket is open!");
    // connection oppened and `Connection` record added to DynamoDB
  };

  // Setup listener for messages via websockets
  socket.onmessage = function(message) {
    var data = JSON.parse(message.data);

    if (data.event_type == "hover") {
      drawDashboard(data, "hovers");
    } else if (data.event_type == "click") {
      drawDashboard(data, "clicks");
    }
  };
});

// TODO: use API Key (or any other Auth methods) when openning connection
// `Sec-WebSocket-Protocol` header can be used to pass the `Authorization` header
// socket = new ReconnectingWebSocket("wss://f61ceyfszl.execute-api.us-east-1.amazonaws.com/dev", ["api_key"]);
// issue is connection gets closed and JS plugin tries to open again and connection is closed again

// alternative:
// socket = new ReconnectingWebSocket("wss://f61ceyfszl.execute-api.us-east-1.amazonaws.com/dev", ["Bearer api key"]);
