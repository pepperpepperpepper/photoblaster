//but I tool a procedural approach, and I wanted to make something more like OOP. just didn't know
//how do deal with the fact that $.fancybox is a class...a singleton class is totally fine. 
//like colorpicker_iframe. just need to know what it would look like 
//well in this case you might not need oop approach, as it doesn't solve any issues here. its fine to use procedural code then you
//don't need oop. also js is sort of using procedural way then asking to provide onclick code and other methods like .click() in jquery, 
//so it's kind of callback\procedural oriented, and oop doesn't fit in very well. you can wrap it in oop if really want, it will look like:
//
//function ColorPicker(){
//  this.element = $(".something");
//  this.init = function(){ 
//     this.options = options
//     this.element.click(this.onclick);
//     this.myfancybox = $.fancybox; 
//     this.myfancybox_iframe = ".fancybox-iframe";
//   }
//  this.onclick = function(){
//    this.myfancybox.open(
//     do I do something like this
//     _.extend({ autoDimensions: false,
//       autoDimensions: false,
//       beforeShow: this.fancybox_cb_1, //something like this? yes ok I think that it's the right thing for methods
//       to reach for these classes for trivial things for a while, so that I can used to thinking this way.
//       I understand that there are no real benefits performance/readability-wise here, but it's a different paradigm, 
//       right? yes ok cool. Well 
//        }, options) //? yep
//
//    this.options
//    ...
//    callback: funciton(){ this.color_picked = ...from fancybox .. }
//    callback: this.callback,
//    );
//  }
//  this.color_picked = function()
//  this.color_picked_as_hex = function()
//  this.color_picked_as_rgb = function()
//  this.callback = function(){
//   $(this.myfancybox_iframe). ....
//  }
//}
//and so on yeah good
//
function launch_iframe(input_target){
  $.fancybox.open({
    href : '/im/colors/index.html',
    width  : 1100,           // set the width
    height : 710,
    fitToView : true,
    autoDimensions:false,
    autoSize:false,
    type : 'iframe',
    closeBtn  : false,
    padding : 5,
    beforeShow : function(){					
      $('.fancybox-iframe').contents().find('#submitvalue').click(function(){
        $('.fancybox-iframe').contents().find('form').submit();						
        $.fancybox.close();
      });					
    },				
    beforeClose : function(){
      x = $('.fancybox-iframe').contents().find('#namespace').val();
    },
    afterClose: function(){
      $(input_target).val(x);
    }
  });
}
$(document).ready(function(){
 if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
   return;
 }
 var element_list = [".color1", ".color2"]
 element_list.forEach(
   function(l){
     console.log("a"+l)
     $("a"+l).click(function(event){ 
       event.preventDefault();
       launch_iframe("input"+l) 
     });
   }
 )
	
})
