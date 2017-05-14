package com.example.usage;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class GreetingTest {

    private Greeting greeting;

    @Before
    public void setUp() {
        greeting = new Greeting();
    }

    @Test
    public void hello_NormalName_HelloSomebody() {
        assertEquals("Hello, Android!", greeting.hello("Android"));
    }

    // @Test
    public void hello_EmptyName_HelloWorld() {
        assertEquals("Hello, World!", greeting.hello(""));
    }

    // @Test
    public void hello_NullName_HelloWorld() {
        assertEquals("Hello, World!", greeting.hello(null));
    }

}
