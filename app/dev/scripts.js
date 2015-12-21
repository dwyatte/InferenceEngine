
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


sigCanvas.bind('outNode', function(e) {
    sigCanvas.graph.nodes().forEach(function(n) {
    	n.label = n.originalLabel;
    	n.color = n.originalColor;
    });

    sigCanvas.graph.edges().forEach(function(e) {
    	e.size = e.originalSize;
     	e.color = e.originalColor;
    });

    sigCanvas.refresh();
});


var doUpdate = function()
{
	console.log("starting update");
	sigma.parsers.json(
		  'data/data.json',
		  sigCanvas,
		  function() {

			sigCanvas.graph.nodes().forEach(function(n) {
				if(n.label[0] == "i")
				{
					n.color = "#00BFFF";
				}
				if(n.label[0] == "l")
				{
					n.color = "#23E3B5";
				}
				if(n.label[0] == "o")
				{
					n.color = "#9370DB";
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
};


doUpdate();
var socket = io.connect('http://localhost:4000');

socket.on('Changed', function(data) {
	console.log("received update signal");
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
});



