var container, stats;
var camera, controls, scene, renderer;
var mesh, texture, material;
//FIXME experiment with these fixed params
var worldWidth = 256, worldDepth = 256, worldHalfWidth = worldWidth / 2, worldHalfDepth = worldDepth / 2;
var textureFile = 'img/Texture.jpg'; 
var heightmapFile = 'img/Heightmap.jpg';
var pos_x, pos_y, pos_z, rot_x, rot_y, rot_z;
var wf = false;


function runWebGLSimulation(){
	//Detect WebGL
	if (!Detector.webgl) {
		Detector.addGetWebGLMessage();
		document.getElementById('container').innerHTML = "";
	}

	//Start Graphics
	initGraphics(textureFile, heightmapFile, function(){ animate() });
	//Start Scene Animation
}

function initGraphics(textureFile, heightmapFile, cb) {

	container = document.getElementById('container');
	//Set camera
	camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 1, 20000);
	//Set scene
	scene = new THREE.Scene();
	
	//Get heightmap data
	//Generates the heightmap data from the heightmap image
	var size = worldWidth * worldDepth, data = new Float32Array(size);

	var canvas = document.createElement('canvas');
	canvas.width = worldWidth;
	canvas.height = worldDepth;
	context = canvas.getContext('2d');
	context.fillStyle = '#000';
	context.fillRect(0, 0, worldWidth, worldDepth);

	var img = new Image();
	img.src = heightmapFile;
  img.onerror = function() { 
    alert("The following url did not work: \n"+heightmapFile.slice(15)); 
    is_generating = false;
    toggle_background();
  };

  img.onload = function(){
    context.drawImage(img, 0, 0);
    image = context.getImageData(0, 0, worldWidth, worldDepth);
    var imageData = image.data;
    var pixels = size;
    for (var i=0; i<pixels; i++){
      // Get RGB
      red = imageData[4 * i + 0];
      green = imageData[4 * i + 1];
      blue = imageData[4 * i + 2];
      // Get grayscale
      gray = (red + green + blue) / 3;
      // Put heightmap value
      data[i] = gray;
    }

    //Set camera position
    camera.position.y = data[worldHalfWidth + worldHalfDepth * worldWidth] + 500;
    scene.add(camera);
    
    //Create geometry data used for mesh
    var geometry = new THREE.PlaneGeometry(7500, 7500, worldWidth - 1,	worldDepth - 1);
    for ( var i = 0, l = geometry.vertices.length; i < l; i++) {
      geometry.vertices[i].position.z = data[i] * 3;
    }
    
    //Load texture
    texture = THREE.ImageUtils.loadTexture(textureFile, {}, function() {
      renderer.render(scene, camera);
    });
    texture.needsUpdate = true;
    
    //Create mesh from heightmap and texture
    material = new THREE.MeshBasicMaterial({
      map : texture,
      wireframe: wf
    });
    mesh = new THREE.Mesh(geometry, material);
    mesh.rotation.x = -90 * Math.PI / 180;
    scene.add(mesh);

    //Create renderer
    renderer = new THREE.WebGLRenderer({
      preserveDrawingBuffer : true // required to support .toDataURL()
    }); 
    renderer.setSize(window.innerWidth, window.innerHeight - 150); //FIXME, add height of the controls
    container.innerHTML = "";
    container.appendChild(renderer.domElement);

    //Get default values
    pos_x = mesh.position.x;
    pos_y = mesh.position.y;
    pos_z = mesh.position.z;
    rot_x = mesh.rotation.x;
    rot_y = mesh.rotation.y;
    rot_z = mesh.rotation.z;
  is_generating = false;
  toggle_background();
  cb();
  };
}

var requestId;
function loop() {
    render();
    requestId = window.requestAnimationFrame(loop);
}
function animate() {
    if (!requestId) {
       loop();
    }
}
function stop_animating() {
    if (requestId) {
       window.cancelAnimationFrame(requestId);
       requestId = undefined;
    }
}


function render() {
	renderer.render(scene, camera);
}

function init_controls(){
  var listener = new window.keypress.Listener();
  var my_scope = this;
  var my_combos = listener.register_many([
      {
          "keys"          : "up",
          "is_solitary"  : true,
          "on_keydown"    : function() {
              mesh.position.y += 150;
          },
          "this"          : my_scope
      },
      {
          "keys"          : "down",
          "is_solitary"  : true,
          "on_keydown"    : function() {
              mesh.position.y -= 150;
          },
          "this"          : my_scope
      },
      {
          "keys"          : "right",
          "is_solitary"  : true,
          "on_keydown"    : function() {
              mesh.position.x += 150;
          },
          "this"          : my_scope
      },
      {
          "keys"          : "left",
          "is_solitary"  : true,
          "on_keydown"    : function() {
              mesh.position.x -= 150;
          },
          "this"          : my_scope
      },
      {
          "keys"          : "shift up",
          "is_exclusive"  : true,
          "on_keydown"    : function() {
              mesh.rotation.x += 0.1;
          },
          "this"          : my_scope
      },
      {
          "keys"          : "shift down",
          "is_exclusive"  : true,
          "on_keydown"    : function() {
              mesh.rotation.x -= 0.1;
          },
          "this"          : my_scope
      },
      {
          "keys"          : "shift right",
          "is_exclusive"  : true,
          "on_keydown"    : function() {
              mesh.rotation.z -= 0.1;
          },
          "this"          : my_scope
      },
      {
          "keys"          : "shift left",
          "is_exclusive"  : true,
          "on_keydown"    : function() {
              mesh.rotation.z += 0.1;
          },
          "this"          : my_scope
      },
      {
          "keys"          : "delete",
          "is_exclusive"  : true,
          "on_keydown"    : function() {
              mesh.position.x = pos_x;
              mesh.position.y = pos_y;
              mesh.position.z = pos_z;
              mesh.rotation.x = rot_x;
              mesh.rotation.y = rot_y;
              mesh.rotation.z = rot_z;
          },
          "this"          : my_scope
      },
      {
          "keys"          : "pageup",
          "is_exclusive"  : true,
          "on_keydown"    : function() {
              mesh.position.z += 150;
          },
          "this"          : my_scope
      },
      {
          "keys"          : "pagedown",
          "is_exclusive"  : true,
          "on_keydown"    : function() {
              mesh.position.z -= 150;
          },
          "this"          : my_scope
      },
      {
          "keys"          : "space",
          "is_exclusive"  : true,
          "on_keydown"    : function() {
              wf = !wf;
              material.wireframe = wf;
          },
          "this"          : my_scope
      },
  ]);
}


window.onload= function(e){
  runWebGLSimulation();
  init_controls();
}
