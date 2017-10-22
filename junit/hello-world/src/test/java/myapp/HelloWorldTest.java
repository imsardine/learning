package myapp;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Map;
import java.io.InputStreamReader;
import java.io.IOException;

import org.junit.Test;
import org.junit.Before;
import org.junit.After;
import static org.junit.Assert.*;

public class HelloWorldTest {

    @Before
    public void setUp() { }

    @After
    public void tearDown() { }

    @Test
    public void sayHello_NoArg_HelloWorld() {
        // Arrange preconditions
        String output = run(); // Act on xxx under test (ex. CUT, AUT, SUT)
        assertEquals("Hello, World!\n", output); // Assert expected results
    }

    @Test
    public void sayHello_SingleArg_HelloFirstArg() {
        assertEquals("Hello, Java!\n", run("Java"));
    }

    @Test
    public void sayHello_SingleArgWithWhitespace_HelloFirstArg() {
        assertEquals("Hello, Java Guys!\n", run("Java Guys"));
    }

    private String run(String... args) {
        try {
            return runImpl(args);
        } catch (IOException | InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    private String runImpl(String... args) throws IOException, InterruptedException {
        ArrayList<String> command = new ArrayList<String>();
        command.addAll(Arrays.asList("java", "myapp.HelloWorld"));
        command.addAll(Arrays.asList(args));

        ProcessBuilder pb = new ProcessBuilder(command);
        Map<String, String> env = pb.environment();
        env.put("CLASSPATH", "build/classes/main");

        Process p = pb.start();
        int exitCode = p.waitFor();
        assert exitCode == 0 : exitCode;

        InputStreamReader input = new InputStreamReader(p.getInputStream());
        StringBuffer buff = new StringBuffer();

        int character;
        while ((character = input.read()) != -1) {
            buff.append((char) character);
        }

        return buff.toString();
    }

}
