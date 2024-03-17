$(document).ready(function() {
  setInterval(function() {
    $.ajax({
      type: "GET",
      url: "https://qxk9fmectf.execute-api.us-east-1.amazonaws.com/dev/v1/stats?action=click",
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", "api_key");
      },
      success: function(data){
        drawDashboard(data, "clicks");
      }
    });
  }, 500);
});
