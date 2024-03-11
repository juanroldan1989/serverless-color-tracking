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
      url: "https://qemn8s86a8.execute-api.us-east-1.amazonaws.com/dev/v1/events",
      data: `{"action_color": { "action_name" : "hover", "color_name" : "${color}" } }`
    });
  });

  // Trigger "click" event
  $("td").click(function(){
    var color = this.className;

    $.ajax({
      type: "POST",
      url: "https://qemn8s86a8.execute-api.us-east-1.amazonaws.com/dev/v1/events",
      data: `{"action_color": { "action_name" : "click", "color_name" : "${color}" } }`
    });
  });
});
