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
    public void only8LowOrderBitsAreWriteen() {
        // The byte to be written is the eight low-order bits of the argument b.
        // The 24 high-order bits of b are ignored.
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        int input = 0b11111111111111111111111101100001; // 'a' = 01100001 (97)
        out.write(input);

        assertEquals(1, out.size());
        assertEquals(out.toByteArray()[0], 0b01100001);
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
    public void writeAllBytes() throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        byte[] bytes = {97, 98, 99}; // abc
        out.write(bytes);

        assertEquals(3, out.size());
        assertArrayEquals(bytes, out.toByteArray());
        assertEquals("abc", out.toString());
    }

    @Test
    public void writePartialBytes() throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        byte[] bytes = {97, 98, 99, 100, 101, 102, 103}; // a b c d e f g
        out.write(bytes, 3, 3);

        byte[] expected = {100, 101, 102}; // bytes[off] ~ bytes[off + len - 1]
        assertArrayEquals(expected, out.toByteArray());
        assertEquals("def", out.toString());
    }

    @Test(expected = Test.None.class)
    public void close_SubsequentOperationsWontThrowExceptions() throws Exception {
        // The methods in this class can be called after the stream has been
        // closed without generating an IOException.
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        byte[] bytes = {97, 98, 99}; // abc
        out.write(bytes);

        out.close();
        assertEquals(3, out.size());

        out.write(bytes);
        assertEquals(6, out.size());
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

