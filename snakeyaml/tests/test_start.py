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

def test_hello_world_javabeans(workspace):
    workspace.src('hello.yml', r'''
    greeting: Hello
    who: World
    ''')

    workspace.src('mypkg/Hello.java', r'''
    package mypkg;

    public class Hello {

      private String greeting;
      private String who;

      public String getGreeting() {
        return greeting;
      }

      public void setGreeting(String greeting) {
        this.greeting = greeting;
      }

      public String getWho() {
        return who;
      }

      public void setWho(String who) {
        this.who = who;
      }

    }
    ''')

    workspace.src('Main.java', '''
    import java.io.FileInputStream;
    import java.util.Map;
    import org.yaml.snakeyaml.Yaml;
    import mypkg.Hello;

    public class Main {
      public static void main(String[] args) throws Exception {
        Hello hello = new Yaml().loadAs(new FileInputStream("hello.yml"), Hello.class);
        System.out.print(hello.getGreeting() + ", " + hello.getWho() + "!");
      }
    }
    ''')

    workspace.run('javac -cp .:/tmp/deps/compile/* Main.java mypkg/Hello.java');
    assert workspace.run('java -cp .:/tmp/deps/compile/* Main').out == 'Hello, World!'
