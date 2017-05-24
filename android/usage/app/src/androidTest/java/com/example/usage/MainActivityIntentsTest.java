package com.example.usage;

import android.support.test.espresso.intent.rule.IntentsTestRule;

import org.junit.Rule;
import org.junit.Test;

import static android.support.test.espresso.Espresso.onView;
import static android.support.test.espresso.action.ViewActions.click;
import static android.support.test.espresso.action.ViewActions.typeText;
import static android.support.test.espresso.intent.Intents.intended;
import static android.support.test.espresso.intent.matcher.IntentMatchers.hasExtra;
import static android.support.test.espresso.intent.matcher.IntentMatchers.isInternal;
import static android.support.test.espresso.matcher.ViewMatchers.withId;
import static org.hamcrest.Matchers.allOf;

public class MainActivityIntentsTest {

    @Rule
    public IntentsTestRule<MainActivity> activityRule = new IntentsTestRule<>(MainActivity.class);

    @Test
    public void hello() {
        onView(withId(R.id.somebody)).perform(typeText("Android"));
        onView(withId(R.id.sayHello)).perform(click());

        // It is surprised that the activity is also launched
        intended(allOf(isInternal(), hasExtra("SOMEBODY", "Android")));
    }

}
