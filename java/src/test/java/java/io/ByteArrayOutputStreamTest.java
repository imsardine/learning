import org.junit.Test;
import static org.junit.Assert.*;
import java.io.ByteArrayOutputStream;

public class ByteArrayOutputStreamTest {

    @Test
    public void initialState() {
        ByteArrayOutputStream out = new ByteArrayOutputStream();

        assertEquals(0, out.size());
        assertArrayEquals(new byte[0], out.toByteArray());
        assertEquals("", out.toString());
    }

    @Test
    public void write() throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        byte[] bytes = {97, 98, 99}; // abc
        out.write(bytes);

        assertEquals(3, out.size());
        assertArrayEquals(bytes, out.toByteArray());
        assertEquals("abc", out.toString());
    }

    @Test
    public void toStringOrToByteArrayMoreThanOnce() throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        byte[] bytes = {97, 98, 99}; // abc
        out.write(bytes);

        assertArrayEquals(bytes, out.toByteArray());
        assertArrayEquals(bytes, out.toByteArray());
        assertEquals("abc", out.toString());
        assertEquals("abc", out.toString());
    }

    @Test
    public void reset() throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        byte[] bytes = {97, 98, 99}; // abc
        out.write(bytes);

        assertEquals(3, out.size());

        out.reset();

        assertEquals(0, out.size());
        assertArrayEquals(new byte[0], out.toByteArray());
        assertEquals("", out.toString());
    }

}

