function route(handle, pathname, request, response) {
  handle = handle[pathname];
  if (typeof handle == "function") {
    handle(response, request); // note the order
  } else {
    response.writeHead(404, {"Content-Type": "text/plain"});
    response.write("404 Not Found.");
    response.end();
  }
}

exports.route = route;

