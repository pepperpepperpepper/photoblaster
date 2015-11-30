var Main =
	{
	API_HEADER: "#@im",
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
		$("#output-cmd").html('generating...').show()
		$("#result").show()
		var data =
			{
			url: $("#img-url").val(),
			transparent: $('#img-transparent:checked').val() !== undefined ? "true" : "false",
			flip: $('#img-flip:checked').val() !== undefined ? "true" : "false",
			flop: $('#img-flop:checked').val() !== undefined ? "true" : "false",
			nearest: $('#img-nearest:checked').val() !== undefined ? "true" : "false",
			rotate: $("#img-rotate").val(),
			subtract: $("#img-subtract").val(),
			fuzz: $("#img-fuzz").val(),
			width: $("#img-width").val(),
			height: $("#img-height").val(),
			black: $("#img-black").val(),
			white: $("#img-white").val(),
			//brightness: $("#img-brightness").val(),
			//saturation: $("#img-saturation").val(),
			hue: $("#img-hue").val(),
			contrast: $("#img-contrast").val(),
			background: $("#img-background").val(),
			// merge_early: $('#img-merge_early:checked').val() !== undefined ? "true" : "false",
			compose: $('#img-compose :selected').text(),
			gravity: $('#img-gravity :selected').text(),
			// tile: $('#img-tile:checked').val() !== undefined ? "true" : "false",
			format: $('#img-format :selected').text(),
			dispose: $('#dispose').val(),
			username: $("#img-name").val(),
			}
		if (data.rotate.match(/-/)){ data.rotate=360-parseInt(data.rotate.replace("-","")); };
		$("#img-rotate").val("");
		if (data.username.length > 0)
			document.cookie = "imname="+data.username+";path=/;domain=.asdf.us;max-age=1086400"
		$.post("/im/api/generate", data, Main.callback)
		},
	error: function (s)
		{
		$("#output-cmd").html("<span class='error'>ERROR: " + s + "</span>").show()
		$("#output-url").hide()
		$("#output-img").hide()
		},
	callback: function (data)
		{
		Main.generating = false
		$("#output-cmd").html("size: "+Main.filesize(data.size)+"<br/>"
      + data.width + " x " + data.height);
       
		$("#output-url").val(data.url);
		$("#output-img").hide().attr("src", data.url).fadeIn(700)
		$("#sendtoinput").html("&nbsp;send to input <img src=\"img/arrow_pointing_left.png\"/>&nbsp;").css({"border": "1px solid gray", "cursor" : "pointer"}).click(function(){
			$("#img-url").val(data.url);
		});
		
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
	preloadSize: function(url,label,tag){
		console.log(url)
		var img = new Image()
		img.onload = function(){ $(label).html( tag + ": " + img.naturalWidth + " x " + img.naturalHeight ) }
		img.src = url
	},
	init: function ()
		{
		var name = Main.cookie ()
		$("#img-name").val(name)
    if (name)
      {
      $("#userlink").show()
      $("#userlink a").attr("href", "/im/gallery/?name="+name).html(name+"'s photoblasts")
      }
    $("#likebutton,#controls").fadeIn(0)
		$("#img-generate").bind("click", Main.go)
		$("div input[type=text]").bind("keydown", Main.enter)
		$("#img-url").change(function(){Main.preloadSize(this.value,"#img-url-label","image")})
		$("#img-background").change(function(){Main.preloadSize(this.value,"#background-url-label","bg")})
		$("#bgswitcheroo").click(function() {
		    a = $("#img-url").val();
	    	    b = $("#img-background").val();
		    $("#img-url").val(b);
	    	    $("#img-background").val(a);
		  });
		$("#colorswitcheroo").click(function() {
		    a = $("#img-white").val();
	    	    b = $("#img-black").val();
		    $("#img-white").val(b);
	            $("#img-black").val(a);
		  });
		$("#img-format").change(function(){
			$("#gif-options").css( "visibility",  $("#img-format").val() === "gif" ? "visible" : "hidden")
		})

		},
	}
document.getElementById('imform').reset();
Main.init ()
