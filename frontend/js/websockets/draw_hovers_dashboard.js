$(document).ready(function() {
  var cable = ActionCable.createConsumer('ws://localhost:3000/v1/events/cable')

  cable.subscriptions.create("HoversChannel", {
    connected: function() {
      console.log("You've subscribed to the Hovers Channel");
    },
    disconnected: function() {
      console.log("You've disconnected from the Hovers Channel");
    },
    received: function (data) {
      drawDashboard(data, "hovers");
    }
  });
});
