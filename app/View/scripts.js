sigma.classes.graph.addMethod('neighbors', function(nodeId) {
var k,
    neighbors = {},
    index = this.allNeighborsIndex[nodeId] || {};

for (k in index)
  neighbors[k] = this.nodesIndex[k];

return neighbors;
});




var firstTime = true;
var sigCanvas = new sigma(
	{
		container: 'graph-Contain',
		renderer: {
			container: document.getElementById('graph-Contain'),
			type: 'canvas'
		},
		settings: 
		{
			defaultLabelColor: "#FFFFFF",
			defaultEdgeColor: "rgb(175,175,175)",
			edgeColor: "default",
			minEdgeSize: 1,
			maxEdgeSize: 2,
			labelThreshold: 9,
			animationsTime: 1000
		},
	});

	

sigCanvas.bind('overNode', function(e) {
    var nodeId = e.data.node.id;
    var neighs = sigCanvas.graph.neighbors(nodeId);
    neighs[nodeId] = e.data.node;

    sigCanvas.graph.nodes().forEach(function(n) {
      if (neighs[n.id])
      {
        n.color = n.originalColor;
      }	
      else
      {
	  	n.color = 'rgb(25,25,25)';
	  	n.label = "";
      }
    });

    sigCanvas.graph.edges().forEach(function(e) {
      if (neighs[e.source] && neighs[e.target])
      {
      	e.size = 2;
    	e.color = "rgb(225,225,225)";
      }
      else
        e.color = 'rgb(25,25,25)';
    });

    sigCanvas.refresh();
});


// sigCanvas.bind('clickStage', function(e){
// 	var nodes = sigCanvas.graph.nodes()
// 	// nodes.forEach(funciton(n){
// 		sigma.plugins.animate(sigCanvas sigma instance,
// 			{
// 			    //property names to be animated to
// 			    x: 'circular_' + 'x',
//       			y: 'circular_' + 'y',
//       		});
// 	// });
	
// })
// var step = 0;

// setInterval(function() {
//   // var prefix = ['grid_', 'circular_'][step = +!step];
//   sigma.plugins.animate(
//     sigCanvas,
//     {
//       x: "condensedX",
//       y: "condensedY",
//     }
//   );
// }, 2000);



sigCanvas.bind('outNode', function(e) {
    sigCanvas.graph.nodes().forEach(function(n) {
    	n.label = n.originalLabel
    	n.color = n.originalColor;
    });

    sigCanvas.graph.edges().forEach(function(e) {
    	e.size = e.originalSize;
     	e.color = e.originalColor;
    });

    sigCanvas.refresh();
});



setInterval(timer, 500);
function timer() {	

	var needsUpdate = "0";
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if(xhttp.readyState == 4 && xhttp.status == 200)
		{
			needsUpdate = xhttp.responseText;
		}
	};
	xhttp.open("GET", "http://localhost:3000/changed", false);
	xhttp.send();

	if(needsUpdate == "1" || firstTime)
	{
		if(!firstTime)
		{
			console.log("HERE");
			sigma.plugins.animate(
			    sigCanvas,
			    {
			      x: "condensedX",
			      y: "condensedY",
			    },
			    {
		    		onComplete: function(){
				    		doUpdate();
				    	}
			    }
			    
		  	);
			    
		}
		else
		{
			doUpdate();
		}


		needsUpdate = "";
		firstTime = false;
	}
	
}


var doUpdate = function()
{
	sigma.parsers.json(
		  'data.json',
		  sigCanvas,
		  function() {

			sigCanvas.graph.nodes().forEach(function(n) {
				if(n.label[0] == "i")
				{
					n.color = "#00BFFF"
				}
				if(n.label[0] == "l")
				{
					n.color = "#23E3B5"
				}
				if(n.label[0] == "o")
				{
					n.color = "#9370DB"
				}
				n.originalLabel = n.label;
				n.originalColor = n.color;
				n.condensedX = 0;
				n.condensedY = 0;
				n.originalX = n.x;
				n.originalY = n.y;
				n.x = n.condensedX;
				n.y = n.condensedY;

			});
			sigCanvas.graph.edges().forEach(function(e) {
				e.originalSize = e.size;
				e.originalColor = e.color;
				e.type = 'curve';

			});
		    sigCanvas.refresh();
		    if(sigCanvas.graph.nodes().length > 0)
			{
				sigma.plugins.animate(
				    sigCanvas,
				    {
				      x: "originalX",
				      y: "originalY",
				    }
		  		);
			}
		  }
		);
}

// var i,
//     s,
//     o,
//     L = 10,
//     N = 100,
//     E = 500,
//     g = {
//       nodes: [],
//       edges: []
//     },
//     step = 0;
// // Generate a random graph:
// for (i = 0; i < N; i++) {
//   o = {
//     id: 'n' + i,
//     label: 'Node ' + i,
//     circular_x: L * Math.cos(Math.PI * 2 * i / N - Math.PI / 2),
//     circular_y: L * Math.sin(Math.PI * 2 * i / N - Math.PI / 2),
//     circular_size: Math.random(),
//     circular_color: '#' + (
//       Math.floor(Math.random() * 16777215).toString(16) + '000000'
//     ).substr(0, 6),
//     grid_x: i % L,
//     grid_y: Math.floor(i / L),
//     grid_size: 1,
//     grid_color: '#ccc'
//   };
//   ['x', 'y', 'size', 'color'].forEach(function(val) {
//     o[val] = o['grid_' + val];
//   });
//   g.nodes.push(o);
// }
// for (i = 0; i < E; i++)
//   g.edges.push({
//     id: 'e' + i,
//     source: 'n' + (Math.random() * N | 0),
//     target: 'n' + (Math.random() * N | 0)
//   });
// // Instantiate sigma:
// s = new sigma({
//   graph: g,
//   container: 'graph-Contain',
//   settings: {
//     animationsTime: 1000
//   }
// });
// setInterval(function() {
//   var prefix = ['grid_', 'circular_'][step = +!step];
//   sigma.plugins.animate(
//     s,
//     {
//       x: prefix + 'x',
//       y: prefix + 'y',
//       size: prefix + 'size',
//       color: prefix + 'color'
//     }
//   );
// }, 2000);