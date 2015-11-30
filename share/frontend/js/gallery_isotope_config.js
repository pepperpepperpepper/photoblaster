
$.Isotope.prototype._getCenteredMasonryColumns = function() {
    this.width = this.element.width();
    
    var parentWidth = this.element.parent().width();
    
                  // i.e. options.masonry && options.masonry.columnWidth
    var colW = this.options.masonry && this.options.masonry.columnWidth ||
                  // or use the size of the first item
                  this.$filteredAtoms.outerWidth(true) ||
                  // if there's no items, use size of container
                  parentWidth;
    
    var cols = Math.floor( parentWidth / colW );
    cols = Math.max( cols, 1 );

    // i.e. this.masonry.cols = ....
    this.masonry.cols = cols;
    // i.e. this.masonry.columnWidth = ...
    this.masonry.columnWidth = colW;
  };
  
  $.Isotope.prototype._masonryReset = function() {
    // layout-specific props
    this.masonry = {};
    // FIXME shouldn't have to call this again
    this._getCenteredMasonryColumns();
    var i = this.masonry.cols;
    this.masonry.colYs = [];
    while (i--) {
      this.masonry.colYs.push( 0 );
    }
  };

  $.Isotope.prototype._masonryResizeChanged = function() {
    var prevColCount = this.masonry.cols;
    // get updated colCount
    this._getCenteredMasonryColumns();
    return ( this.masonry.cols !== prevColCount );
  };
  
  $.Isotope.prototype._masonryGetContainerSize = function() {
    var unusedCols = 0,
        i = this.masonry.cols;
    // count unused columns
    while ( --i ) {
      if ( this.masonry.colYs[i] !== 0 ) {
        break;
      }
      unusedCols++;
    }
    
    return {
          height : Math.max.apply( Math, this.masonry.colYs ),
          // fit container to columns that have been used;
          width : (this.masonry.cols - unusedCols) * this.masonry.columnWidth
        };
  };


//and once the jquery has loaded...
$(function(){
    
    var $container = $('#images');
    
    
      // add randomish size classes
      $container.find('.pb').each(function(){
        var $this = $(this);
        
        number = parseInt( $this.height(), 10 );
        if ( number % 7 % 2 === 1 ) {
          $this.addClass('width2');
        }
        if ( number % 3 === 0 ) {
          $this.addClass('height2');
        }
      });
    
    $container.isotope({
      itemSelector : '.pb',
      sortAscending : false, 
      masonry : {
        columnWidth : 120
      },
      getSortData : {
        date : function( $elem ) {
          src = $elem.attr('src');
          var re = /_[0-9]{10}/g;
          var matches = src.match(re)

          // what.. getting null here -jl 20132712
          if (! matches) return 0;
          for (var i=0;i<matches.length;i++){
            matches[i] = matches[i].replace(/_/g,"");
          }
          //mite be wrong FIXME?
          matches.sort(function(a,b){return b-a});
          return matches[0];
          
        },
        username : function( $elem ) {
          return $elem.attr('username');
        },
        height : function( $elem ) {
          return $elem.height(); 
        },
        width : function( $elem ) {
          return $elem.width();
        },
        gif : function ( $elem ) {
          src = $elem.attr('src');
          var re = /\.gif$/;
          if (re.test(src)){
            return 1;
          }else{
            return 0;
          }
        
        }
      }
    });
    var sorter = {
      date: function(){$container.isotope({sortBy: "date"})},
      username: function(){$container.isotope({sortBy: "username"})},
      height: function(){$container.isotope({sortBy: "height"})},
      width: function(){$container.isotope({sortBy: "width"})},
      gif:function(){$container.isotope({sortBy: "gif"})},
      shuffle: function(){$container.isotope("shuffle")},
      lombada: function(){
        var min = 4; var max = 14;
        var limit =  Math.floor(Math.random() * (max - min + 1)) + min;

        var count = 0;
        var t = setInterval(function(){
          $container.isotope("shuffle")
          if (count == limit){
            clearInterval(t);
          }
          count += 1;
        }, 100)

      }
    }


    $(".sorting-options").each(function(){
      var $this = $(this);
      $this.click(function(){
        var func = $this.attr("id")
        sorter[func]();
      })
    });

//        $container.isotope( 'insert', $newEls );
//        $container.append( $newEls ).isotope( 'appended', $newEls );
     // change size of clicked element
      $container.delegate( '.bg', 'click', function(){
        //FIXME add css here
        $(this).toggleClass('large');
        $container.isotope('reLayout');
      });

      // toggle variable sizes of all elements
      $('#toggle-sizes').find('a').click(function(){
        $container
        //FIXME add css here
          .toggleClass('variable-sizes')
          .isotope('reLayout');
        return false;
      });
     $(document).ready(function(){ sorter.date();  $container.isotope('reLayout');});
   $("img").load(function(){ 
     $(this).css("display", "inline-block");
     $container.isotope('reLayout'); 
   }) 
   window.onload = function(){
      $(".isotope, .isotope .isotope-item").css({
        "-webkit-transition-duration": "0.8s",
        "-moz-transition-duration": "0.8s",
        "-ms-transition-duration": "0.8s",
        "-o-transition-duration": "0.8s",
        "transition-duration": "0.8s"
        
      });
   };

  });

