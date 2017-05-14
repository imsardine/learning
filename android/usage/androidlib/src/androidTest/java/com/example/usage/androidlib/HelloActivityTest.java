package com.example.usage.androidlib;

import android.support.test.InstrumentationRegistry;
import android.support.test.rule.ActivityTestRule;

import org.junit.Rule;
import org.junit.Test;

import static android.support.test.espresso.Espresso.onView;
import static android.support.test.espresso.assertion.ViewAssertions.matches;
import static android.support.test.espresso.matcher.ViewMatchers.withId;
import static android.support.test.espresso.matcher.ViewMatchers.withText;

public class HelloActivityTest {

    @Rule
    public ActivityTestRule<HelloActivity> activityRule = new ActivityTestRule<>(HelloActivity.class, false, false);

    @Test
    public void hello_NormalName_HelloSomebody() {
        activityRule.launchActivity(HelloActivity.prepareIntent(InstrumentationRegistry.getTargetContext(), "Android"));
        onView(withId(R.id.greeting)).check(matches(withText("[AndroidLib] Hello, Android!")));
    }

    @Test
    public void hello_NullName_HelloWorld() {
        activityRule.launchActivity(HelloActivity.prepareIntent(InstrumentationRegistry.getTargetContext(), null));
        onView(withId(R.id.greeting)).check(matches(withText("[AndroidLib] Hello, World!")));
    }

    @Test
    public void hello_EmptyName_HelloWorld() {
        activityRule.launchActivity(HelloActivity.prepareIntent(InstrumentationRegistry.getTargetContext(), ""));
        onView(withId(R.id.greeting)).check(matches(withText("[AndroidLib] Hello, World!")));
    }

}
