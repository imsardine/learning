def test_hello_world(workspace):
    workspace.src('hello.yml', r'''
    greeting: Hello
    who: World
    ''')

    workspace.src('Main.java', '''
    import java.io.FileInputStream;
    import java.util.Map;
    import org.yaml.snakeyaml.Yaml;

    public class Main {
      public static void main(String[] args) throws Exception {
        Map yaml = (Map) new Yaml().load(new FileInputStream("hello.yml"));
        System.out.print(yaml.get("greeting") + ", " + yaml.get("who") + "!");
      }
    }
    ''')

    workspace.run('javac -cp .:/tmp/deps/compile/* Main.java');
    assert workspace.run('java -cp .:/tmp/deps/compile/* Main').out == 'Hello, World!'
