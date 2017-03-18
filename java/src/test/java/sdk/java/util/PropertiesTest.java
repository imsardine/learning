package io.github.imsardine.learning.java;

import org.junit.Test;
import org.junit.Before;
import org.junit.After;
import static org.junit.Assert.*;
import java.io.InputStream;
import java.io.IOException;
import java.util.Properties;

public class PropertiesTest {

    private Properties props;

    @Before
    public void setUp() {
        props = new Properties();
        InputStream in = PropertiesTest.class.getResourceAsStream("prefs.properties");
        assert in != null;
       
        try {
            props.load(in);
        } catch (IOException e) {
            throw new RuntimeException(e);
        } finally {
            if (in != null) {
                try {
                    in.close();
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
        }
    }

    @Test
    public void emptyAndTerminators() {
        assertEquals("", props.getProperty("empty_with_terminator"));
        assertEquals("", props.getProperty("empty_without_terminator"));
    }

    @Test
    public void BothKeyAndValueContainingWhiteSpaces() {
        assertEquals("value containing white spaces", props.getProperty("key containing white spaces"));
    }

    @Test
    public void valueContainingBackslashes() {
        assertEquals("path\\to\\windows\\dir", props.getProperty("backslash"));
    } 

    @Test
    public void multilineValue() {
        assertEquals("line 1\nline 2\nline 3", props.getProperty("multiline"));
    }

    @Test
    public void unicodeValue() {
        assertEquals("你好", props.getProperty("unicode"));
    }

    @Test
    public void quotesInValueAreNotNeeded() {
        // values containing quotes are not what you expect
        assertEquals("\"quotes are treated as a part of value itself.\"", props.getProperty("quotes"));
    }

}
