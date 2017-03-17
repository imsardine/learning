import org.junit.Test;
import org.junit.Before;
import org.junit.After;
import static org.junit.Assert.*;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class StringFormattingTest {

    private ByteArrayOutputStream out = new ByteArrayOutputStream();

    private ByteArrayOutputStream err = new ByteArrayOutputStream();

    @Before
    public void repalceSystemOutAndErr() {
        System.setOut(new PrintStream(out));
        System.setErr(new PrintStream(err));
    }

    @After
    public void resetSystemOutAndErr() {
        System.setOut(null);
        System.setErr(null);
    }

    @Test
    public void captureSystemOutput() {
        System.out.println("Output via System.out.println()");
        System.err.println("Output via System.err.println()");
        assertEquals("Output via System.out.println()\n", out.toString());
        assertEquals("Output via System.err.println()\n", err.toString());
    }

}
