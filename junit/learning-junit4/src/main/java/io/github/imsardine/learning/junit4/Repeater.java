package io.github.imsardine.learning.junit4;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.lang.annotation.ElementType;
import java.util.concurrent.TimeUnit;
import org.junit.rules.TestRule;
import org.junit.rules.Timeout;
import org.junit.runners.model.TestTimedOutException;
import org.junit.runners.model.Statement;
import org.junit.runner.Description;

public class Repeater implements TestRule {

    public Statement apply(Statement base, Description description) {
        Repeat repeat = description.getAnnotation(Repeat.class);

        if (repeat != null) {
            int times = repeat.times();
            long durationMillis = repeat.durationMillis();
            // TODO check times and durationMillis are not specified at the same time

            return createRepeatStatement(times, durationMillis, base, description);
        } else {
            return base;
        }
    }

    @Retention(RetentionPolicy.RUNTIME)
    @Target(ElementType.METHOD)
    public static @interface Repeat {
        int times() default 0;
        long durationMillis() default 0;
    }

    private Statement createRepeatStatement(final int times, long durationMillis,
            final Statement base, Description description) {
        final Statement loop = Timeout.millis(durationMillis).apply(new Statement() {
            public void evaluate() throws Throwable {
                int counter = times;
                do {
                    base.evaluate();
                } while (times == 0 || --counter != 0);
            }
        }, description);

        if (durationMillis == 0) {
            return loop;
        } else {
            return new Statement() {
                public void evaluate() throws Throwable {
                    try {
                        loop.evaluate();
                    } catch (TestTimedOutException ex) { }
                }
            };
        }
    }

}

