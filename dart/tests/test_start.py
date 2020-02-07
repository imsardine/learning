def test_hello_world(workspace):
    workspace.src('helloworld.dart', '''
    void main() {
      print('Hello, World!');
    }
    ''')

    assert workspace.run('dart helloworld.dart').out == 'Hello, World!'
