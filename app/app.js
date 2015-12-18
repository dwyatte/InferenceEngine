var express = require('express');
var app = express();
var fs = require("fs");
var $ = require('jquery');
var http = require('http');

var filename = "data/data.json";
// var filename = "foo.gexf";
var changed = "0";


fs.watchFile(filename, {
  persistent: true
}, function(event, filename) {
	changed = "1";
});


app.use(express.static(__dirname + '/dist'));

// respond with "hello world" when a GET request is made to the homepage
app.get('/', function(req, res) {
  res.sendFile('index.html');
});

app.get('/changed', function(req, res) {
	res.send(changed);
	changed = "0";
})


var server = app.listen(3000, function () {
  console.log('Example app listening on port 3000');
});