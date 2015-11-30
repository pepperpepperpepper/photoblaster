var is_generating = false;
function toggle_background(){
 if (is_generating){
   $('body').css("background", "url(img/generating_background.gif)");
 }else{
   $('body').css("background", "whitesmoke");
 }
}
