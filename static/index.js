window.onload = () => {
  var url_string = window.location;
  var url = new URL(url_string);
  var id = url.searchParams.get("id");
  var siteId = url.searchParams.get("siteId");
  console.log(id)
  $("#sendbutton").click(() => {
    imagebox = $("#imagebox");
    imagebox2 = $("#imagebox2");

    input = $("#imageinput")[0];
    if (input.files && input.files[0]) {
      let formData = new FormData();
      formData.append("video", input.files[0]);
      formData.append("id", id);
      formData.append("siteId", siteId);
      $.ajax({
        url: "http://127.0.0.1:5000/detect", // fix this to your liking
        type: "POST",
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        error: function (data) {
          console.log("upload error", data);
          console.log(data.getAllResponseHeaders());
        },
        success: function (data) {
            console.log(data);
            imagebox.attr('src' , 'http://127.0.0.1:5000/static/'+ data)
            imagebox2.attr('src' , 'http://127.0.0.1:5000/static/static-worker/'+ data)
            imagebox2.height(500);
            imagebox2.width(800);
            console.log(data);
        },
      });
    }
    
  });
};

function readUrl(input) {
  imagebox = $("#imagebox");
  imagebox2 = $("#imagebox2");
  console.log(imagebox);
  console.log("evoked readUrl");
  if (input.files && input.files[0]) {
    let reader = new FileReader();
    reader.onload = function (e) {
      console.log(e.target);

      imagebox.attr("src", e.target.result);
         imagebox.height(500);
         imagebox.width(800);
      
    };
    imagebox2.attr('src' , '')
    imagebox2.height(0);
    imagebox2.width(0);
    reader.readAsDataURL(input.files[0]);
  }
}
