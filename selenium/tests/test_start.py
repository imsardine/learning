from selenium import webdriver

def test_hello_world(workspace):
    workspace.src('index.html', """
    <html>
    <head>
      <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    </head>
    <body>
      <p>Hello, <span id="who">...</span>!</p>
      <script>
          $('#who').html('World');
      </script>
    </body>
    </html>
    """)

    try:
        driver = webdriver.Firefox()
        driver.get('file:///' + workspace.workdir + '/index.html')
        e = driver.find_element_by_tag_name('p')
        assert e.text == 'Hello, World!'
    finally:
        driver.quit()
