package io.github.imsardine.learning.junit4;

import org.junit.rules.TestRule;
import org.junit.runners.model.Statement;
import org.junit.runner.Description;
import java.util.logging.Logger;

public class TestLogger implements TestRule {

    private static final Logger logger = Logger.getLogger(TestLogger.class.getName());

    private Logger testLogger;

    public Logger getLogger() {
        return logger;
    }

    public Statement apply(final Statement base, final Description description) {
        return new Statement() {
            public void evaluate() throws Throwable {
                testLogger = Logger.getLogger(description.getTestClass().getName());
                logger.info("Test logger created, start invoking inner statement.");
                base.evaluate();
                logger.info("After invoking inner statement.");
            }
        };
    }

}
