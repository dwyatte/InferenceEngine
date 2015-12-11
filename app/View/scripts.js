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
			defaultNodeColor: "#ec5148",
			defaultEdgeColor: "#ec5148",
			edgeColor: "default",
			minEdgeSize: 1,
			maxEdgeSize: 3
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
	  	n.color = '#eee';
	  	n.label = "";
      }
    });

    sigCanvas.graph.edges().forEach(function(e) {
      if (neighs[e.source] && neighs[e.target])
      {
      	e.size = 3;
    	e.color = e.originalColor;
      }
      else
        e.color = '#eee';
    });

    sigCanvas.refresh();
});


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



setInterval(timer, 1000);
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
		console.log("DRAWING");
		sigma.parsers.json(
		  'data.json',
		  sigCanvas,
		  function() {
		  	console.log(sigCanvas.graph.nodes())
			sigCanvas.graph.nodes().forEach(function(n) {
				n.originalLabel = n.label;
				n.originalColor = n.color;
			});
			sigCanvas.graph.edges().forEach(function(e) {
				e.originalSize = e.size;
				e.originalColor = e.color;
				e.type = 'curve';

			});
		    sigCanvas.refresh();
		  }
		);



		needsUpdate = "";
		firstTime = false;
	}
	
}

