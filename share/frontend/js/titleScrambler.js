var titleSwitch = true;
var FillerChars = [ "(",")","|","1","4","\\", "9","_" ];
var titleArray = document.title.split("");
var titleArrayCopy = titleArray.slice(0);
var titleLength = titleArray.length

function marqueeArray(arr){
  var first = arr[0]
  arr.shift()
}

function replaceArray(arr, char){
  arr[randomChoice(arr)] = char
}
var titleUpdateInterval = 300
function randomChoice(arr){
  var rand = Math.random();
  rand *= arr.length;
  rand = Math.floor(rand)
  return rand;
}
var titleUpdate = setInterval(function(){
    if (titleSwitch === true){ 
    marqueeArray(titleArray); 
    document.title = titleArray.join("")
    if (titleArray.length === 1){
      document.title = "";
      titleArray = titleArrayCopy.slice(0);
      document.title = titleArray.join("");
      if (titleSwitch){
        titleSwitch = false;
      }else{
        titleSwitch = true;
        titleUpdateInterval = 100;
      }
    } 
    }else{

    replaceArray(titleArray, FillerChars[randomChoice(FillerChars)]);
    document.title = titleArray.join("")
    if (titleArray[(titleArray.length-1)] in FillerChars){
      console.log("it's in there");
      titleArray = titleArrayCopy.slice(0);
      document.title = titleArray.join("");
      if (titleSwitch){
        titleSwitch = false;
        titleUpdateInterval = 300;
      }else{
        titleSwitch = true;
      }
      
    }
  } 
    
  }, titleUpdateInterval);

