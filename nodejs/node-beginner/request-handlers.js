var fs = require("fs")
  , formidable = require("formidable");

function start(response) {
  console.log("start called.");
  var body =
    '<html>' +
    '<body>' +
    '<form action="upload" method="post" enctype="multipart/form-data">' +
    '<input type="file" name="upload" />' +
    '<input type="submit" value="Upload File" />' +
    '</form>' +
    '</body>' +
    '</html>';
  response.writeHead(200, {'Content-Type': 'text/html'});
  response.write(body);
  response.end();
}

function upload(response, request) {
  console.log("upload called.");
  var form = new formidable.IncomingForm();
  form.parse(request, function(error, fields, files) {
    fs.rename(files.upload.path, "/tmp/test.png");
    response.writeHead(200, {'Content-Type': 'text/html'});
    response.write('<img src="/show" />');
    response.end();
  });
}

function show(response) {
  console.log("show called.");
  response.writeHead(200, {'Content-Type': 'image/png'});
  fs.createReadStream("/tmp/test.png").pipe(response); 
  // response.end();
}

exports.start = start
exports.upload = upload
exports.show = show

