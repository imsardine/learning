def test_hello_world(workspace):
    workspace.src('Hello.java', '''
    public class Hello {
      public static void main(String[] args) {
        System.out.print("Hello, World!");
      }
    }
    ''')

    workspace.run('javac Hello.java');
    assert workspace.run('java Hello').out == 'Hello, World!'
