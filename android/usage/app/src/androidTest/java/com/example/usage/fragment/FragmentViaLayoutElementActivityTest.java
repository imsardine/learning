package com.example.usage.fragment;

import android.support.test.rule.ActivityTestRule;

import org.junit.Rule;
import org.junit.Test;

import static android.support.test.espresso.Espresso.onView;
import static android.support.test.espresso.assertion.ViewAssertions.matches;
import static android.support.test.espresso.matcher.ViewMatchers.isDisplayed;
import static android.support.test.espresso.matcher.ViewMatchers.withText;

public class FragmentViaLayoutElementActivityTest {

    @Rule
    public ActivityTestRule<FragmentViaLayoutElementActivity> activityTestRule = new ActivityTestRule<>(FragmentViaLayoutElementActivity.class);

    @Test
    public void fragmentIsDisplayed() throws Exception {
        onView(withText("Fragment A")).check(matches(isDisplayed()));
    }

}
