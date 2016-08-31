package io.github.imsardine.learning.hamcrest;

import junit.framework.TestCase;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;
import java.util.Collection;
import java.util.ArrayList;

public class BasicTest extends TestCase {

    public void testAssertThat() {
        assertEquals(4, 2 + 2); // assertEquals(expected, actual)
        assertThat(2 + 2, equalTo(4)); // assertThat(actual, matcher)
        assertThat("2 plus 1", 2 + 2, not(equalTo(5))); // assertThat(reason, actual, matcher)
    }

    public void testAnything() {
        assertThat(1, anything());
        assertThat(null, anything());
    }

    public void testIs() {
        assertThat(null, is(anything())); // is(matcher) => more expressive
        assertThat("string", is(String.class)); // deprecated, use isA(type) instead
        assertThat("str" + "ing", is("string")); // is(value) = is(equalTo(value))
    }

    public void testLogicalMatchers() {
        assertThat(5, allOf(greaterThan(4), lessThan(6)));
        assertThat(5, anyOf(greaterThan(6), lessThan(6)));
        assertThat(5, not(anyOf(lessThan(5), greaterThan(5))));
    }

    public void testTypeMatchers() {
        // type
        assertThat(ArrayList.class, typeCompatibleWith(Collection.class));
        assertThat(Collection.class, not(typeCompatibleWith(ArrayList.class)));
    }

    public void testInstanceMatchers() {
        // instance
        assertThat(new ArrayList(), instanceOf(Collection.class));
        assertThat(new ArrayList(), isA(Collection.class)); // isA = is(instanceOf(type))
        assertThat(null, not(instanceOf(Collection.class)));

        // identity
        assertThat("string", sameInstance("string"));
    }

    public void testNullMatchers() {
        assertThat(null, nullValue());
        assertThat(new Object(), notNullValue()); 
        assertThat(new Object(), not(nullValue())); 
    }

    public void testStringMatchers() {
        String greeting = "Hello, World!";
        assertThat(greeting, startsWith("Hello"));
        assertThat(greeting, endsWith("!"));
        assertThat(greeting, containsString("World"));
        assertThat(greeting, not(containsString("world"))); // case sensitive
        assertThat(greeting, equalToIgnoringCase("hello, world!"));

        assertThat(greeting, equalToIgnoringWhiteSpace("Hello,  World!")); // collapsed
        assertThat(greeting, not(equalToIgnoringWhiteSpace("Hello,World!")));
    }

    public void testBooleanMatchers() {
        assertThat(2 > 1, is(true));
        assertThat(2 < 1, is(false));
        assertThat(2 < 1, not(true));
    }

}
