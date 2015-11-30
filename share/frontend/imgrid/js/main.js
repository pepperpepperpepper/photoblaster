var Main =
	{
	API_HEADER: "#@imgrid",
	generating: false,
	enter: function (e)
		{
		if (Main.generating)
			return
		if (e.keyCode === 13)
			Main.go()
		},
	go: function ()
		{
		if (Main.generating)
			return
		Main.generating = true
		var theloader = '<span style="width:100%;margin-right:40%"><img style="width:140px;height:120px;display:inline;" src="img/generating.gif"></img></span>'
		$("#output-cmd").html(theloader).show()
		if($('#transition :selected').val() === 'tile'||$('#transition :selected').val()=== 'random')
			{
			$('#output-cmd').append("<br><span style='color:red'>WARNING: THIS REQUEST MIGHT TAKE A WHILE</span>")
			}
		$('.results').show()
		$("#output-img").show()
		$("#output-url").show()
		$("#result").show()
		var data =
			{
			width: $("#img-width").val(),
			height: $("#img-height").val(),
			linethickness: $("#line-thickness").val(),
			opacity: $("#line-opacity").val(),
			linecolor: $("#line-color").val(),
			spacing: $("#line-spacing").val(),
			vlines: $('#v-lines:checked').val() !== undefined ? "true" : "false",
			hlines: $('#h-lines:checked').val() !== undefined ? "true" : "false",
			shadow: $('#shadow:checked').val() !== undefined ? "true" : "false",
			bgimage: $("#bg-image").val(),
			bgcolor: $("#bg-color").val(),
			imageinstead: $("#imageinstead").val(),
			planebgcolor: $("#planebgcolor").val(),
			skycolor: $("#skycolor").val(),
			planebgimage: $("#planebgimage").val(),
			transition: $('#transition :selected').val(),
			swing: $("#swing").val(),
			tilt: $("#tilt").val(),
			roll: $("#roll").val(),
			zoom: $("#zoom").val(),
			trim: $("#trim:checked").val() !== undefined ? "true" : "false",
			finalformat: $('#format :selected').val(),
			username: $('#username').val()
			}
		if (data.transition == 'infinite'){
		$('#genbutton').append("<span style='color:red'>WARNING:This might take a while</span>")}
		if (data.username.length > 0)
		document.cookie = "imname="+data.username+";path=/;domain=.asdf.us;max-age=1086400"
		$.post("/im/api/imgrid", data, Main.callback)
		},
	error: function (s)
		{
		$("#output-cmd").html("<span class='error'>ERROR: " + s + "</span>").show()
		$("#output-url").hide()
		$("#output-img").hide()
		},
	filesize: function (size)
		{
		if (size < 1024)
			return size.toString() + " bytes"
		if (size < 1024 * 1024)
			return Math.floor (size/1024).toString() + " KB"
		else
			return Math.floor (size/(1024*1024)).toString() + " MB"
		},
	callback: function (data)
		{
		$("#output-cmd").html('')
		$("#output-img").html("<a target=_blank href='"+data.url+"'>"+"<img src='"+data.url+"'></img><br>"+"</a>");
		$("#output-url").val(data.url)
		$("#output-info").html('-ACTUAL SIZE-<br>'+Main.filesize(data.size)+'<br>'+data.width+'<br>'+data.height+'<br><br>'+'<span style="float:right">see more at &rarr;<a href="http://asdf.us/im/gallery">photoblaster gallery</a></span>'+'<br>')
		Main.generating = false
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
		$("#username").val(name)
    if (name)
      {
//      $("#userlink").show()
  //    $("#userlink a").attr("href", "/im/gallery/?name="+name).html(name+"'s photoblasts")
      }
		$("#generate").bind("click", Main.go)
		$(document).bind("keydown", Main.enter)
		}
	}
$('#theform').each(function(){
	        this.reset();
											});



Main.init ()
