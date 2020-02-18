def test_config_object_without_javabean_mapping(workspace):
    workspace.src('hello.yml', r'''
    greeting: Hello
    year: 2020
    ''')

    workspace.src('Main.java', '''
    import java.io.FileInputStream;
    import java.util.Map;
    import org.yaml.snakeyaml.Yaml;
    import mypkg.Config;
    import mypkg.ConfigImpl;

    public class Main {
      public static void main(String[] args) throws Exception {
        Map settings = (Map) new Yaml().load(new FileInputStream("hello.yml"));
        Config config = new ConfigImpl(settings);
        System.out.print(config.getGreeting() + ", Y" + config.getYear() + "!");
      }
    }
    ''')

    workspace.src('mypkg/Config.java', r'''
    package mypkg;

    public interface Config {
      String getGreeting();
      int getYear();
    }
    ''')

    workspace.src('mypkg/ConfigImpl.java', r'''
    package mypkg;

    import java.util.Map;

    public class ConfigImpl implements Config {

      private Map settings;

      public ConfigImpl(Map settings) {
        this.settings = settings;
      }

      public String getGreeting() {
        return (String) settings.get("greeting");
      }

      public int getYear() {
        return (Integer) settings.get("year");
      }

    }
    ''')

    workspace.run('javac -cp .:/tmp/deps/compile/* Main.java mypkg/Config.java mypkg/ConfigImpl.java');
    assert workspace.run('java -cp .:/tmp/deps/compile/* Main').out == 'Hello, Y2020!'

