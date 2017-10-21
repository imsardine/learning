package myapp;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Map;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.IOException;

import org.junit.Test;
import org.junit.Before;
import org.junit.After;
import static org.junit.Assert.*;

public class HelloTest {

    @Before
    public void setUp() { }

    @After
    public void tearDown() { }

    @Test
    public void run_NoArg_HelloWorld() {
        assertEquals("Hello, World!\n", run());
    }

    @Test
    public void run_SingleArg_HelloFirstArg() {
        assertEquals("Hello, Java!\n", run("Java"));
    }

    @Test
    public void run_MultipleArgs_HelloFirstArg() {
        assertEquals("Hello, Java!\n", run("Java", "Unit", "Testing"));
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
        command.addAll(Arrays.asList("java", "myapp.Hello"));
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
