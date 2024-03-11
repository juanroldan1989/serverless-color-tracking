$(document).ready(function() {
  var cable = ActionCable.createConsumer('ws://localhost:3000/v1/events/cable')

  cable.subscriptions.create("ClicksChannel", {
    connected: function() {
      console.log("You've subscribed to the Clicks Channel");
    },
    disconnected: function() {
      console.log("You've disconnected from the Clicks Channel");
    },
    received: function (data) {
      drawDashboard(data, "clicks");
    }
  });
});
