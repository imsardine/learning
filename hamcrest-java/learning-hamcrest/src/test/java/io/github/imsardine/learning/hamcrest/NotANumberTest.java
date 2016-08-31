package io.github.imsardine.learning.hamcrest;

import junit.framework.TestCase;
import static org.hamcrest.MatcherAssert.*;
import static org.hamcrest.Matchers.*;
import static io.github.imsardine.learning.hamcrest.NotANumber.notANumber;

public class NotANumberTest extends TestCase {

    public void testMatche() {
        assertThat(Math.sqrt(-1), notANumber());
    }

    public void testMismatch() {
        try{
            assertThat(0.1, notANumber());
        } catch (AssertionError ex) {
            assertThat(ex.getMessage(), startsWith("\nExpected: not a number\n     but: was <0.1>"));
        }
    }

}
