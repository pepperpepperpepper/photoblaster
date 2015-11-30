



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
 var element_list = [".img-white", ".img-black", ".img-subtract"]
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
