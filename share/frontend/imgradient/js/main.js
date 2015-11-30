	$(function() {
		$( "#blur-slider" ).slider({
			value:0,
			min: 0,
			max: 20,
			step: 1,
			slide: function( event, ui ) {
				$( "#img-blur" ).val(ui.value);
			}
		});
		$( "#img-blur" ).val( $( "#blur-slider" ).slider( "value" ) );
		
		$( "#brightness-slider" ).slider({
			value:100,
			min: 0,
			max: 200,
			step: 1,
			slide: function( event, ui ) {
				$( "#img-brightness" ).val(ui.value);
			}
		});
		$( "#img-brightness" ).val( $( "#brightness-slider" ).slider( "value" ) );

		$( "#hue-slider" ).slider({
			value:100,
			min: 0,
			max: 200,
			step: 1,
			slide: function( event, ui ) {
				$( "#img-hue" ).val(ui.value);
			}
		});
		$( "#img-hue" ).val($( "#hue-slider" ).slider( "value" ) );

		$( "#saturation-slider" ).slider({
			value:100,
			min: 0,
			max: 200,
			step: 1,
			slide: function( event, ui ) {
				$( "#img-saturation" ).val(ui.value);
			}
		});
		$( "#img-saturation" ).val($( "#saturation-slider" ).slider( "value" ) );
	});

var Main =
	{
	API_HEADER: "#@imgradient",
	enter: function (e)
		{
//    console.log("calling enter")
    if (e.keyCode === 13){
      Main.go()
    }
		},
	go: function ()
		{
		$("#output-cmd").html('generating...').show()
		$("#result").show()
		var data =
			{
			flip: $('#img-flip:checked').val() !== undefined ? "true" : "false",
			flop: $('#img-flop:checked').val() !== undefined ? "true" : "false",
			tilt: $('#img-tilt').val(),
			rotate: $("#img-rotate").val(),
			subtract: $("#img-subtract").val(),
			width: $("#img-width").val(),
			height: $("#img-height").val(),
			color2: $("#img-color2").val(),
			color1: $("#img-color1").val(),
			brightness: $("#img-brightness").val(),
			saturation: $("#img-saturation").val(),
			blurriness: $("#img-blur").val(),
			hue: $("#img-hue").val(),
			contrast: $("#img-contrast").val(),
			gradienttype: $('#gradient-type :selected').val(),
			bevel: $('#bevel-type :selected').val(),
			percentbeveled: $('#percentbeveled').val(),
			halftone: $('#halftone-type :selected').val(),
			stripes: $('#stripes:checked').val() !== undefined ? "true" : "false",
			stripenumber: $('#stripenumber').val(),
			stripeintensity: $('#stripeintensity').val(),
			format: $('#img-format :selected').text(),
			name: $("#img-name").val(),
			}
    if (data.name.length > 0){
			document.cookie = "imname="+data.name+";path=/;domain=.asdf.us;max-age=1086400"
    }
    $.post("/im/api/imgradient", data, Main.callback)
    $("#controls").css('margin',"")
		},
	error: function (s)
		{
		$("#output-cmd").html("<span class='error'>ERROR: " + s + "</span>").show()
		$("#output-url").hide()
		$("#output-img").hide()
		},
	callback: function (data)
    {
      if (data.error){
        return Main.error(data.error)
      }
      $("#output-cmd").html("size: "+Main.filesize(data.size)+"<br/>"+data.height + "&nbsp;x&nbsp;" + data.width)
      $("#output-url").val(data.url)
      $("#output-img").hide().attr("src", data.url).fadeIn(700)
    },
	filesize: function (size)
		{
		if (size < 1024)
			return size + " bytes"
		if (size < 1024 * 1024)
			return Math.floor (size/1024) + " KB"
		else
			return Math.floor (size/(1024*1024)) + " MB"
		},
	cookie: function ()
		{
		if (document.cookie)
			{
			var cookies = document.cookie.split(";")
			for (i in cookies)
				{
				var cookie = cookies[i].split("=")
				if (cookie[0].indexOf("imname") !== -1)
					{
					if (cookie[1] !== 'false' && cookie[1] !== 'undefined' && cookie[1].length)
						{
						return cookie[1]
						}
					}
				}
			}
		return ""
		},
	init: function ()
		{
		var name = Main.cookie ()
		$("#img-name").val(name)
		},
}

$(document).ready(function(){
  Main.init ()
  $('form').submit(function() {
    return false;
  });
	$(document).keydown(Main.enter)
	$("#img-generate").click(Main.go)
  document.getElementById("reset").reset()
})
