$(document).ready(function() {

  // Display "hover" effect on table cell colors
  $("td")
    .mouseenter(function() {
      var color = $(this).attr("class");
      var hoverColor = "dark" + color;
      $(this).css("background-color", hoverColor);
    })
    .mouseleave(function() {
      var color = $(this).attr("class");
      $(this).css("background-color", color);
    });

  // Trigger "hover" event
  $("td").mouseenter(function(){
    var color = this.className;

    $.ajax({
      type: "POST",
      url: "https://qxk9fmectf.execute-api.us-east-1.amazonaws.com/dev/v1/events",
      data: `{ "action" : "hover", "color" : "${color}" }`,
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", "api_key");
      }
    });
  });

  // Trigger "click" event
  $("td").click(function(){
    var color = this.className;

    $.ajax({
      type: "POST",
      url: "https://qxk9fmectf.execute-api.us-east-1.amazonaws.com/dev/v1/events",
      data: `{ "action" : "click", "color" : "${color}" }`,
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", "api_key");
      }
    });
  });
});
