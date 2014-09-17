var http = require("http")
  , url = require("url");

function start(route, handle) {
  http.createServer(function(request, response) {
    pathname = url.parse(request.url).pathname;
    route(handle, pathname, request, response);
  }).listen(8080);
}

exports.start = start;

