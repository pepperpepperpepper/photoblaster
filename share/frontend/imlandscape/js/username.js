$(document).ready(function(){
  var name = get_name_from_cookie()
  $("#username").val(name)
});

function get_name_from_cookie()
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
};

function update_username(username){
  if (username.length > 0){
    document.cookie = "imname="+username+";path=/;domain=.asdf.us;max-age=1086400"
  }
}
