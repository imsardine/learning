package com.example.buildvariants;

import org.junit.Test;
import static org.junit.Assert.*;

public class GreetingTest {

    @Test
    public void greet() {
        // this assertion only works with prod flavor.
        assertEquals("Hello, World!", Greeting.greet());
    }

}
