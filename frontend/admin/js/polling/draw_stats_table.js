$(document).ready(function() {
  setInterval(function() {
    $.ajax({
      type: "GET",
      url: "https://qxk9fmectf.execute-api.us-east-1.amazonaws.com/dev/admin/v1/stats",
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", "admin_api_key");
      },
      success: function(data){
        console.log("admin - draw table - data: ", data);
        $.each( data.stats, function( key, data ) {
          console.log("admin - draw table - data: ", data);

          // data = {
          //   "api_key" : "api_key",
          //   "action" : "hover",
          //   "counts" : [
          //     {'action': 'hover', 'color': 'blue', 'count': 317},
          //     {'action': 'hover', 'color': 'green', 'count': 308},
          //     {'action': 'hover', 'color': 'yellow', 'count': 286},
          //     {'action': 'hover', 'color': 'red', 'count': 308}
          //   ]
          // }

          $.each(data.counts, function(key, val) {
            updateCell(data.api_key, data.action, val.color, val.count);
          });
        });
      }
    });
  }, 500);
});
