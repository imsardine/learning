package io.github.imsardine.learning.junit4;

import org.junit.Test;
import org.junit.Rule;
import org.junit.Before;
import org.junit.After;
import org.junit.rules.Timeout;

public class TimeoutRuleTest {

    @Rule
    public Timeout timeout = Timeout.millis(3000);

    @Test
    public void infiniteLoop() throws InterruptedException {
        while (true) {
            Thread.sleep(1000);
            System.out.println("...");
        }
    }

    @Before
    public void setUp() {
        System.out.println("==============> BEGIN");
        }

    @After
    public void tearDown() {
        System.out.println("==============> END");
    }

}
