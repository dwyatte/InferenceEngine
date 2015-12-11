

var test = new sigma(
	{
		container: 'container',
		settings: 
		{
		  defaultNodeColor: '#ec5148',
		}
	});

console.log(test);

setInterval(timer, 1000);


function timer() {
	console.log("HERE");
	sigma.parsers.json(
	  'test.json',
	  test,
	  function() {
	    test.refresh();
	  }
	);
}

