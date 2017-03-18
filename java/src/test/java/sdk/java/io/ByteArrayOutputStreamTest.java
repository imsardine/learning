package sdk.java.io;

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
    public void writeAllBytes() throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        byte[] bytes = {97, 98, 99}; // abc
        out.write(bytes);

        assertEquals(3, out.size());
        assertArrayEquals(bytes, out.toByteArray());
        assertEquals("abc", out.toString());
    }

    @Test
    public void writeSingleByte() throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        out.write(97);
        out.write(98);
        out.write(99);

        assertEquals(3, out.size());
        assertEquals("abc", out.toString());
    }

    @Test
    public void writePartialBytes() throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        byte[] bytes = {97, 98, 99, 100, 101, 102, 103}; // a b c d e f g
        out.write(bytes, 3, 3);

        byte[] expected = {100, 101, 102};
        assertArrayEquals(expected, out.toByteArray());
        assertEquals("def", out.toString());
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

