$(function(){ 

// test if Photoblaster is being loaded in an iframe (=dump.fm) or not
var isEmbed = window != window.parent; 

if(isEmbed) {
  
  /*
   * jQuery postMessage - v0.5 - 9/11/2009
   * http://benalman.com/projects/jquery-postmessage-plugin/
   * 
   * Copyright (c) 2009 "Cowboy" Ben Alman
   * Dual licensed under the MIT and GPL licenses.
   * http://benalman.com/about/license/
   */
  (function($){var g,d,j=1,a,b=this,f=!1,h="postMessage",e="addEventListener",c,i=b[h]&&!$.browser.opera;$[h]=function(k,l,m){if(!l){return}k=typeof k==="string"?k:$.param(k);m=m||parent;if(i){m[h](k,l.replace(/([^:]+:\/\/[^\/]+).*/,"$1"))}else{if(l){m.location=l.replace(/#.*$/,"")+"#"+(+new Date)+(j++)+"&"+k}}};$.receiveMessage=c=function(l,m,k){if(i){if(l){a&&c();a=function(n){if((typeof m==="string"&&n.origin!==m)||($.isFunction(m)&&m(n.origin)===f)){return f}l(n)}}if(b[e]){b[l?e:"removeEventListener"]("message",a,f)}else{b[l?"attachEvent":"detachEvent"]("onmessage",a)}}else{g&&clearInterval(g);g=null;if(l){k=typeof m==="number"?m:typeof k==="number"?k:100;g=setInterval(function(){var o=document.location.hash,n=/^#?\d+&/;if(o!==d&&n.test(o)){d=o;l({data:o.replace(n,"")})}},k)}}}})(jQuery);
  
  /* end postMessage */
  
  var parent_url = decodeURIComponent( document.location.hash.replace( /^#/, '' ) );
  
  // add click-to-dump to output image
  $('#output-img').live("click", function(){
    $.postMessage(JSON.stringify({'command':'paste_url_to_dump_msginput', 'url':$(this).attr('src')}), parent_url, parent );
  });
  
  // listen for a command from the parent.
  $.receiveMessage(function(e){
    try{
      var data = JSON.parse(e.data)
  
      if ( data.command == 'image_url' ) {

    	$("#img-url").val(data.url);
  
        $("#img-url").prev().css('background-color', 'white');
        $("#img-background").prev().css('background-color', 'white');
  
       } else if ( data.command == 'background_url' ) {

    	 $("#img-background").val(data.url);
  
         $("#img-url").prev().css('background-color', 'white');
         $("#img-background").prev().css('background-color', 'white');
  
       } else if ( data.command == 'img_drag' ) {

         // highlight while dragging to show which field this drag will go to
         $("#img-background").prev().css('background-color', 'white');
         $("#img-url").prev().css('background-color', 'yellow'); 

       } else if ( data.command == 'background_drag' ) {

         $("#img-url").prev().css('background-color', 'white');
         $("#img-background").prev().css('background-color', 'yellow'); 

       }
     }catch(e){
  	   console.log('receiveMessage (iframe): JSON parse error');
     }  
  });
  
} //isEmbed
});

