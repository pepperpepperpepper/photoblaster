$(function(){
  for (var i=0; i< (imagedata.length - 1); i++){
    var newDiv = document.createElement("div");
    var newImage = document.createElement("img");
    newImage.src = imagedata[i][0];
    newImage.className = "pb";
    newDiv.appendChild(newImage);
//    consider calling something like isotope add here...and ONLY APPENDING the image to the parent div once it has loaded
//    $(newImage).load(function(){
//    })
    $("#images").append(newDiv);
  }
});

$(function(){
  $("b").addClass("pulsate_and_grow");
  $(".sorting-options").click(function(){

  $(".sorting-options").click(function(){
    if ($(this).hasClass("pulsate_opacity")){
      $(this).removeClass("pulsate_opacity");
    }
    $(this).addClass("pulsate_opacity");

  });
  });
});


//ZeroClipboard.setMoviePath( 'http://asdf.us/swf/ZeroClipboard10.swf' );
//var clip = new ZeroClipboard.Client();
//clip.glue( 'd_clip_button' );

var Dump = {
  pick: function ()
    {
    Dump.pickUrl( $(this).attr("src") )
    },
  pickUrl: function (url)
    {
    $("#rebus").append ($ ("<img>").attr ("src", url))
    $("#rebus").show()
    var theDump = $("#urlz").val() + " " + url
    $("#urlz").val( theDump )
//    clip.setText( theDump )
    return false
    },
  clear: function ()
    {
    $("#rebus").html("")
    $("#urlz").val("")
//    clip.setText("")
    },
  backspace: function ()
    {
    $("#rebus img:last").remove()
    var urllist = $("#urlz").val().split(" ")
    urllist.pop()
    $("#urlz").val( urllist.join(" ") )
    },
  reverse: function ()
    {
    urllist = $("#urlz").val().split(" ")
    Dump.clear()
    for (i in urllist.reverse())
      if (urllist[i])
        Dump.pickUrl(urllist[i])
    },
  showNewer: function()
    {
    },
  showOlder: function()
    {
    }
}

function applyTag(tagname){
  tag_regex = /&tag=[^&]*/;
  if (document.URL.match(tag_regex)){
    return document.URL.replace(tag_regex, "&tag="+tagname);
  }else if(document.URL.match(/\/$/)){
     return document.URL.replace(/\/$/, "?tag="+tagname);
  }
  else{
    return document.URL+"&tag="+tagname;
  }
}
var Main =
  {
  editing: false,
  kp: function (event)
    {
    switch (event.keyCode)
      {
      // BS
      case 8:
        if (! Main.editing)
          Dump.backspace()
        return false
      // C
      case 67:
        if (! Main.editing)
          Dump.clear()
        break
      // R
      case 82:
        if (! Main.editing)
          Dump.reverse()
        break
      // ESC
      case 27:
      // H
      case 72:
        if (! Main.editing)
          $("#rebus").toggle()
        break
      // LEFT ARROW
      case 37:
        if (! Main.editing)
          Dump.showNewer()
        break
      // RIGHT ARROW
      case 39:
        if (! Main.editing)
          Dump.showOlder()
        break
      }
    return true
    },
  poll: function ()
    {
    },
  pollCallback: function ()
    {
    },
  init: function ()
    {
    $(document).keydown(Main.kp)
    $("#urlz").focus(function(){ Main.editing = true })
    $("#urlz").blur(function(){ Main.editing = false })
    $("#clear").live("click", Dump.clear)
    $("#help").click(function(){ $("#keys").slideToggle() })
    $("#actions b").click(function(){ $("#sorting-optionsContainer").slideToggle() })
    $("#tags b").click(function(){ $("#tag-optionsContainer").slideToggle() })
    $(".tag-options").click(function(){document.location.href= applyTag(this.id)});
    $(".tag-clear").click(function(){ document.location.href = document.URL.replace(/&?tag=[^&]*/ ,"").replace(/\?$/,"")});
    $("div img").live("click", Dump.pick)
    Dump.clear()
    }
  }




$(function(){
  //get params from the query string, and create
  //the back and newer buttons
  //taking into account name, tag and random
  var params = {
    name
  }
  Main.init()
})
