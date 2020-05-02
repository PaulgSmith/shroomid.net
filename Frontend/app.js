var albumBucketName = "shroomid-live-test";
var bucketRegion = "us-west-2";
var IdentityPoolId = "us-west-2:29c0be5d-174f-463d-abfe-fdcfed0c9d08";

AWS.config.update({
  region: bucketRegion,
  credentials: new AWS.CognitoIdentityCredentials({
    IdentityPoolId: IdentityPoolId
  })
});

var s3 = new AWS.S3({
  apiVersion: "2006-03-01",
  params: { Bucket: albumBucketName}
});

function getHtml(template) {
   return template.join('\n');
}

function show_image(src, width, height, alt) {
    document.getElementById("shroom").src = src;
    document.getElementById("shroom").width = width;
    document.getElementById("shroom").height = height;
    document.getElementById("shroom").alt = alt;
}

function addPhoto(albumName) {
  var files = document.getElementById("photoupload").files;
  if (!files.length) {
    alert("Please choose a file to upload first.");
    return new Promise(function (){return 1});
  }
  var file = files[0];
  var fileName = file.name;
  var albumPhotosKey = encodeURIComponent(albumName) + "//";
  var photoKey = albumPhotosKey + fileName;
  // Use S3 ManagedUpload class as it supports multipart uploads
  var upload = new AWS.S3.ManagedUpload({
    params: {
      Bucket: albumBucketName,
      Key: photoKey,
      Body: file,
      ACL: "public-read"
    }
  });
  var promise = upload.promise();
  return promise;
}

function resetResults() {
    document.getElementById("res").innerHTML = "";
    document.getElementById("shroom").src = "img/userTest.png";
    document.getElementById("results-container").style.opacity = "0";
}

function show_results(arrItems) {
  if (parseFloat(arrItems[0].score) < .3){
    show_image("img/fail.png", 200, 200, "Low Results");
    document.getElementById("res").innerHTML += "<center>Scores were too low</center>";
  }
  else{
  show_image(arrItems[3].Location, 200, 200, "Results");
  var i;
  var len = arrItems.length -1;
  document.getElementById("res").innerHTML +=  "<center>" + arrItems[0].name + "</center><br>"

  for (i = 0; i < len; i++) {
    document.getElementById("res").innerHTML += "Name: " + arrItems[i].name +
    "(" + arrItems[i].score + ")<br>";
    }
  }
  document.getElementById("results-container").style.opacity = "1";
  //var div = document.getElementById("results-container");
  //div.className = "results-container";
}

function api_gateway_put(args) {
  resetResults();
  document.getElementById("res").innerHTML = "";
  $.ajax({
    method: 'POST',
    url: 'https://98lw99osmi.execute-api.us-west-2.amazonaws.com/DeepLearning_Lambda',
    data: JSON.stringify(args),
    contentType: 'application/json',
  })
  .done((res) => {
    if (!res) {
      console.log('Incorrect. Please try again.');
    }
    document.getElementById("photoupload").value = ""
    show_results(res);
    $("#myButton").attr("disabled", false);
    // Used to reset the "loaded file"
  })
  .catch((err) => {
    $('.answer').html('Something went terribly wrong!');
    console.log(err);
  })
}
