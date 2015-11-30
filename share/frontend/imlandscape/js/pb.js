var saveUrl = '/im/api/PbLandscape';
var textureURL, heightmapURL;
function saveScene(){
	if (!renderer) {
		alert("WebGL Rendering was not started yet!");
	} else {
		// Prepare data
		var imageData = renderer.domElement.toDataURL("image/png");
		//Remove header
		var seconds = new Date() / 1000;
		seconds = seconds.toFixed(0);
		var userName = $("#username").val()
    update_username(userName);
		var filename;
		if (!userName) {
			filename = seconds + "_imlandscape";
		} else {
			filename = seconds + "_imglandscape_" + userName;
		}
		filename += ".png";
	  is_generating = true;	
    toggle_background();
		// Send post request
	    $.post(
            saveUrl, 
		        { 
              name: $("#username").val(), //FIXME
              imgdata: imageData,
              texture: $("#texture").val(),
              heightmap: $("#heightmap").val(),
            },
		        function(response) {
               console.log(response);
               is_generating = false;
               toggle_background();
               loadUrlResult(response['url'])
		        }
		); 		
	}
}

function loadUrlResult(url){
  $(".url_result").show();
  url_shortened = "...."+ url.slice(url.length-10);

  $("a.url_result").attr("href", url);
  $("a.url_result").html(url_shortened);
  
};
function loadNew() {
	//Get values for url
	textureURL = document.getElementById("texture").value.replace(/\s/,"");
	heightmapURL = document.getElementById("heightmap").value.replace(/\s/,"");
	
  is_generating = true;
  toggle_background();
  console.log(textureURL);
  console.log(heightmapURL);
    stop_animating();
    var new_texture = '/proxy?url='+textureURL;
    var new_heightmap = '/proxy?url='+heightmapURL;
    initGraphics(new_texture, new_heightmap, function(){ animate() } );
}

function isUrl(s) {
	var regexp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?\.(jpg|JPG|jpeg|JPEG)/;
	return regexp.test(s);
}
