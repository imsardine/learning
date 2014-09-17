var server = require("./server.js")
  , router = require("./router.js")
  , requestHandlers = require('./request-handlers.js');

var handle = {};
handle["/"] = requestHandlers.start
handle["/start"] = requestHandlers.start
handle["/upload"] = requestHandlers.upload
handle["/show"] = requestHandlers.show

server.start(router.route, handle);

