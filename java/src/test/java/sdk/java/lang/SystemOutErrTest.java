package sdk.java.lang;

import org.junit.Test;
import org.junit.Before;
import org.junit.After;
import static org.junit.Assert.*;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class SystemOutErrTest {

    private ByteArrayOutputStream out = new ByteArrayOutputStream();

    private ByteArrayOutputStream err = new ByteArrayOutputStream();

    private PrintStream systemOut;

    private PrintStream systemErr;

    @Before
    public void repalceSystemOutAndErr() {
        // Backup
        systemOut = System.out;
        systemErr = System.err;

        System.setOut(new PrintStream(out));
        System.setErr(new PrintStream(err));
    }

    @After
    public void resetSystemOutAndErr() {
        // Restore. `System.setOut(null)` or `System.setErr(null)` will cause NPE.
        System.setOut(systemOut);
        System.setErr(systemErr);
    }

    @Test
    public void printlnViaOutAndErr() {
        System.out.println("Output via System.out.println()");
        System.err.println("Output via System.err.println()");
        assertEquals("Output via System.out.println()\n", out.toString());
        assertEquals("Output via System.err.println()\n", err.toString());
    }

}
