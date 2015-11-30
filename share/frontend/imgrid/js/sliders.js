  $(function() {
    $( "#line-thickness-slider" ).slider({
      value:1,
      min: 0,
      max: 300,
      step: 1,
      slide: function( event, ui ) {
        $( "#line-thickness" ).val(ui.value);
            }
        });
    $( "#line-thickness" ).val( $( "#line-thickness-slider" ).slider( "value" ) );
    $( "#opacity-slider" ).slider({
      value:1,
      min: 0,
      max: 1,
      step: .1,
      slide: function( event, ui ) {
        $( "#line-opacity" ).val(ui.value);
            }
        });
    $( "#line-opacity" ).val( $( "#opacity-slider" ).slider( "value" ) );
    $( "#spacing-slider" ).slider({
      value:10,
      min: 1,
      max: 400,
      step: 1,
      slide: function( event, ui ) {
        $( "#line-spacing" ).val(ui.value);
      }
        });
    $( "#line-spacing" ).val( $( "#spacing-slider" ).slider( "value" ) );

    $( "#swingslider" ).slider({
      value:0,
      min: -180,
      max: 180,
      step: 1,
      slide: function( event, ui ) {
        $( "#swing" ).val(ui.value);
      }
        });
    $( "#swing" ).val( $( "#swingslider" ).slider( "value" ) );

    $( "#tiltslider" ).slider({
      value:0,
      min: -180,
      max: 180,
      step: 1,
      slide: function( event, ui ) {
        $( "#tilt" ).val(ui.value);
                }
          });
    $( "#tilt" ).val( $( "#tiltslider" ).slider( "value" ) );

    $( "#rollslider" ).slider({
      value:0,
      min: -180,
      max: 180,
      step: 1,
      slide: function( event, ui ) {
        $( "#roll" ).val(ui.value);
          }
        });
    $( "#roll" ).val($( "#rollslider" ).slider( "value" ) );

    $( "#zoomslider" ).slider({
      value: 0,
      min: -50,
      max: 50,
      step: .05,
      slide: function( event, ui ) {
				thevalue = (ui.value/4).toFixed(2);
				if (thevalue <= 1 && thevalue >= -1)
					{
					thevalue = 0;
					}
        $( "#zoom" ).val(thevalue);
        		}
				});
    $( "#zoom" ).val($( "#zoomslider" ).slider( "value" ) );
    });
//end sliders jquery

