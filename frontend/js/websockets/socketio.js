$(document).ready(function() {
  const socket = io("wss://knyevievfi.execute-api.us-east-1.amazonaws.com/dev", {
    reconnectionDelayMax: 10000,
    auth: {
      "api_key": "api_key",
      "Access-Control-Allow-Origin": "yes"
    },
    query: {
      "event_type": "click"
    }
  });

  // listening for the `message` event from the server
  socket.on("message", text => {
    console.log("text: ", text);
  })
});
