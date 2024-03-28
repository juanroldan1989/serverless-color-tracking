$(document).ready(function() {

  $("#simulate").click(function(){
    var API_KEYS = [];
    for (var i = 0; i < 100; i++) {
      // Generate random API keys between value 1 and 2
      // API_KEYS.push(Math.floor(Math.random() * 2) + 1);
      API_KEYS.push(i.toString());
      // API_KEYS.push(Math.random().toString(36).substring(2, 10));
    }

    API_KEYS.forEach(function(api_key) {
      var socket;

      // Websocket connection opened
      socket = new ReconnectingWebSocket("wss://0invmqfqdc.execute-api.us-east-1.amazonaws.com/dev");

      socket.onopen = function(event) {
        console.log("Socket is open!");
        // API Key associated with the connection
        data = { "action": "add_api_key", "api_key" : api_key };
        socket.send(JSON.stringify(data));
      };

      for (var i = 0; i < 100; i++) {
        var action = Math.random() < 0.5 ? "click" : "hover";
        var color = ["red", "green", "blue", "yellow"][Math.floor(Math.random() * 4)];

        $.ajax({
          type: "POST",
          url: "https://jj91r76tnd.execute-api.us-east-1.amazonaws.com/dev/v1/events",
          data: `{ "action" : "${action}", "color" : "${color}" }`,
          beforeSend: function (xhr) {
            xhr.setRequestHeader("Authorization", api_key);
          }
        });
      }

      socket.close();
    });
  });

});