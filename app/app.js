var express = require('express');
var app = express();
var chokidar = require('chokidar');
var $ = require('jquery');
var http = require('http');

var ioApp = express();
var ioServer = http.createServer(ioApp);
var io = require('socket.io')(ioServer);

var filename = "data/data.json";


var watcher = chokidar.watch(filename, { persistent: true});




app.use(express.static(__dirname + '/dist'));

app.get('/', function(req, res) {
  res.sendFile('index.html');
});



var server = app.listen(3000, function () {
  console.log('Application listening on port 3000');
});


ioServer.listen(4000, function() {
	console.log("IOServer listening on port 4000");
});

io.on('connection', function (socket) {
	watcher.on('change', function(){
		socket.emit('Changed', "");
	});
});


