var Main =
	{
	firsttime: true,
	generating: false,
	thelast: "",
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
		var theloader = '<span style="width:100%;margin-right:40%"><img style="width:140px;height:120px;display:inline;" src="generating.gif"></img></span>'
		$("#output-cmd").html(theloader).show()
		$('.result').show()
		$('.results').show()
		$("#output-img").show()
		$("#output-url").show()
		$("#result").show()
		var data =
			{
			breakmode:$('input:radio[name=modeswitch]:checked').val(),
			breaktype: $('#breaktype :selected').val(),
			breakangle: $("#breakangle").val(),
			url: $('#url').val(),
			username: $('#username').val(),
//			firsttime: Main.firsttime.toString()
			}
		if (data["breakmode"] == "gradual")
				{
				data["breakmode"] = "subtle"
				if (Main.lines && Main.thelast == $('#url').val())
					{
					Main.firsttime = false
					data["url"] = Main.lines[1]
					}
				}
		else
			{
			Main.firsttime = true
			}
		Main.thelast = $('#url').val();
		thestring = JSON.stringify(data);
		$('#error').append(thestring);
		if (data.username.length > 0)
		document.cookie = "imname="+data.username+";path=/;domain=.asdf.us;max-age=1086400"
		var request = $.ajax({
      type: "POST", 
      url: "/im/api/imbreak",
      data: data, 
      dataType: "json"

    })
    request.done(function(data){
      Main.callback(data)
    })
    request.fail(function(){
      Main.error("The image became too broken!");
      Main.generating = false
    });
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
		$('#error').append('called');
		$("#output-cmd").html('')
		$('#output-url').val(data.url)
		$("#output-img").html("click image to enlarge<br><a target=_blank href='"+data.url+"'>"+"<img src='"+data.url+"' id='output-image'></img><br>"+"</a>"
);
		$("#output-info").html('-ACTUAL SIZE-<br>'+Main.filesize(data.size)+'<br>'+data.width+'<br>'+data.height+'<br><br>'+'<span>see more at &rarr;<a href="http://asdf.us/im/gallery">photoblaster gallery</a></span>'+'<br>')
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
		$("#breakbutton").bind("click", Main.go)
		$(document).bind("keydown", Main.enter)
		}
	}
//$('#theform').each(function(){
//	        this.reset();
//											});



Main.init ()
