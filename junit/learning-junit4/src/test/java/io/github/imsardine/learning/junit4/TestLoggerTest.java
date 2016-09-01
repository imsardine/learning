package io.github.imsardine.learning.junit4;

import org.junit.Test;
import org.junit.Rule;

public class TestLoggerTest {

    @Rule
    public TestLogger logger = new TestLogger();

    @Test
    public void usage() {
        logger.getLogger().warning("testing...");
    }

}

