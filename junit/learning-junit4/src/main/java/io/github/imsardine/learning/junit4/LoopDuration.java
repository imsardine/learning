package io.github.imsardine.learning.junit4;

import org.junit.rules.TestRule;
import org.junit.rules.Timeout;
import org.junit.runners.model.TestTimedOutException;
import org.junit.runners.model.Statement;
import org.junit.runner.Description;
import java.util.concurrent.TimeUnit;

public class LoopDuration implements TestRule {

    private Timeout timeout;

    public LoopDuration(long timeout, TimeUnit timeUnit) {
        this.timeout = new Timeout(timeout, timeUnit);
    }

    public Statement apply(Statement base, Description description) {
        final Statement loop = timeoutLoop(base, description);
        return new Statement() {
            public void evaluate() throws Throwable {
                try {
                    loop.evaluate();
                } catch (TestTimedOutException ex) { }
            }
        };
    }

    private Statement timeoutLoop(final Statement base, Description description) {
        return timeout.apply(new Statement() {
            public void evaluate() throws Throwable {
                while (true) {
                    base.evaluate();
                }
            }
        }, description);
    }

}

