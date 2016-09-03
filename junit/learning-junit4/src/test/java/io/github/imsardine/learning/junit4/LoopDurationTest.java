package io.github.imsardine.learning.junit4;

import org.junit.Test;
import org.junit.Rule;
import java.util.concurrent.TimeUnit;

public class LoopDurationTest {

    @Rule
    public LoopDuration loopDuration = new LoopDuration(3, TimeUnit.SECONDS);

    @Test
    public void usage() throws InterruptedException {
        int TEST_STEPS = 10;

        while (true) {
            for (int i = 1; i < TEST_STEPS; i++) {
                System.out.println("[TEST] Step " + i + " / " + TEST_STEPS + " ...");
                Thread.sleep(500);
            }
        }
    }

}

