package com.example.usage.androidlib;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class LibGreetingTest {

    private LibGreeting greeting;

    @Before
    public void setUp() {
        greeting = new LibGreeting();
    }

    @Test
    public void hello_NormalName_HelloSomebody() {
        assertEquals("[AndroidLib] Hello, Android!", greeting.hello("Android"));
    }

    // @Test
    public void hello_EmptyName_HelloWorld() {
        assertEquals("[AndroidLib] Hello, World!", greeting.hello(""));
    }

    // @Test
    public void hello_NullName_HelloWorld() {
        assertEquals("[AndroidLib] Hello, World!", greeting.hello(null));
    }


}
