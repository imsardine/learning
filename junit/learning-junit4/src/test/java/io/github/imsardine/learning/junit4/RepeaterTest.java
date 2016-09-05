package io.github.imsardine.learning.junit4;

import org.junit.Test;
import org.junit.Rule;
import org.junit.After;
import org.junit.Before;
import java.util.concurrent.TimeUnit;

public class RepeaterTest {

    @Rule
    public Repeater Repeater = new Repeater();

    @Before
    public void setUp() {
        System.out.println("[TEST] Set up ...");
    }

    @After
    public void tearDown() {
        System.out.println("[TEST] Tear down ...");
    }

    @Test
    @Repeater.Repeat(durationMillis = 5000)
    public void forADuration() throws InterruptedException {
        int TEST_STEPS = 3;

        for (int i = 1; i <= TEST_STEPS; i++) {
            System.out.println("[TEST] Duration: Step " + i + " / " + TEST_STEPS + " ...");
            Thread.sleep(500);
        }
    }

    @Test
    @Repeater.Repeat(times = 2)
    public void forManyTimes() throws InterruptedException {
        int TEST_STEPS = 3;

        for (int i = 1; i <= TEST_STEPS; i++) {
            System.out.println("[TEST] Times: Step " + i + " / " + TEST_STEPS + " ...");
            Thread.sleep(100);
        }
    }

    @Test
    public void notRepeated() {
        System.out.println("NOT repeated.");
    }

}

