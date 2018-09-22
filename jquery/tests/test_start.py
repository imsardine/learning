def test_hello_world(workspace):
    workspace.src('index.html', '''
    <html>
    <head>
      <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
      <script>
        $(function() {
          $('#who').html('World');
          console.log($('#greeting').text());
        });
      </script>
    </head>
    <body>
      <p id="greeting">Hello, <span id="who">...</span>!</p>
    </html>
    ''')

    r = workspace.browse('index.html')
    assert (r.out, r.err) == ('Hello, World!\n', '')
