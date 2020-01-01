import re

def test_getresource__jar__jar_file_protocol(workspace):
    workspace.src('App.java', '''
    public class App {
      public static void main(String[] args) {
        System.out.print(App.class.getResource("resource.txt"));
      }
    }
    ''')
    workspace.src('resource.txt', 'content')

    workspace.run('javac App.java')
    workspace.run('jar -cfe app.jar App App.class resource.txt')

    r = workspace.run('java -jar app.jar')
    assert re.match("jar:file:/tmp/.+/app.jar!/resource.txt", r.out)

def test_getresource__outof_jar__file_protocol(workspace):
    workspace.src('App.java', '''
    public class App {
      public static void main(String[] args) {
        System.out.print(App.class.getResource("resource.txt"));
      }
    }
    ''')
    workspace.src('resource.txt', 'content')

    workspace.run('javac App.java')
    r = workspace.run('java App')
    assert re.match("file:/tmp/.+/resource.txt", r.out)
