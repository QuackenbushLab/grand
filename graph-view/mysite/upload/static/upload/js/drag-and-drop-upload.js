$(function () {

  $(".js-upload-upload2").click(function () {
    $("#fileupload2").click();
  });

  $("#fileupload2").fileupload({
    dataType: 'json',
    done: function (e, data) {
      if (data.result.is_valid) {
        $("#gallery tbody").prepend(
          "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
        )
      }
    }
  });

});
