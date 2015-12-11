var express = require('express');
var app = express();
var fs = require("fs");

var filename = "foo.gexf";

fs.watch(filename, {
  persistent: true
}, function(event, filename) {
  console.log(event + " event occurred on " + filename);
});

app.use(express.static(__dirname + '/View'));

// respond with "hello world" when a GET request is made to the homepage
app.get('/', function(req, res) {
  res.sendFile('index.html');
});


var server = app.listen(3000, function () {
  var host = server.address().address;
  var port = server.address().port;

  console.log('Example app listening on port 3000');
});