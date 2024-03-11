$(document).ready(function() {
  // Hovers Dashboard
  setInterval(function() {
    $.ajax({
      type: "GET",
      url: "https://qemn8s86a8.execute-api.us-east-1.amazonaws.com/dev/v1/stats?action=hover",
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", "api_key");
      },
      success: function(data){
        drawChart(data, "hovers");
      }
    });
  }, 500);
});
