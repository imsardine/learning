package io.github.imsardine.learning.hamcrest;

import org.hamcrest.TypeSafeMatcher;
import org.hamcrest.Description;

public class NotANumber extends TypeSafeMatcher<Double> {

    @Override
    public boolean matchesSafely(Double number) {
        return number.isNaN();
    }

    public void describeTo(Description description) {
        description.appendText("not a number");
    }

    public static NotANumber notANumber() {
        return new NotANumber();
    }

}
