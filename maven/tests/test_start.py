def test_hello_world(workspace):
    workspace.src('pom.xml', r'''
    <project>
      <modelVersion>4.0.0</modelVersion>

      <groupId>com.mycompany.app</groupId>
      <artifactId>my-app</artifactId>
      <version>1.0-SNAPSHOT</version>

      <properties>
        <maven.compiler.source>1.7</maven.compiler.source>
        <maven.compiler.target>1.7</maven.compiler.target>
      </properties>

      <dependencies>
        <dependency>
          <groupId>junit</groupId>
          <artifactId>junit</artifactId>
          <version>4.12</version>
          <scope>test</scope>
        </dependency>
      </dependencies>
    </project>
    ''')

    workspace.src('src/main/java/com/mycompany/app/App.java', r'''
    package com.mycompany.app;

    public class App {
      public static void main(String[] args) {
        System.out.print("Hello, World!");
      }
    }
    ''')

    workspace.run('mvn package');
    assert workspace.run('java -cp target/my-app-1.0-SNAPSHOT.jar com.mycompany.app.App').out == 'Hello, World!'
