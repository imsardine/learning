package com.example.usage.fragment;

import android.support.test.rule.ActivityTestRule;
import android.view.View;

import com.example.usage.R;

import org.hamcrest.Matcher;
import org.junit.Rule;
import org.junit.Test;

import static android.support.test.espresso.Espresso.onView;
import static android.support.test.espresso.assertion.ViewAssertions.matches;
import static android.support.test.espresso.matcher.ViewMatchers.isDisplayed;
import static android.support.test.espresso.matcher.ViewMatchers.withChild;
import static android.support.test.espresso.matcher.ViewMatchers.withId;
import static android.support.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;

public class FragmentViaLayoutElementActivityTest {

    @Rule
    public ActivityTestRule<FragmentViaLayoutElementActivity> activityTestRule = new ActivityTestRule<>(FragmentViaLayoutElementActivity.class);

    @Test
    public void fragmentIsDisplayed() {
        Matcher<View> button = withId(R.id.button);
        onView(button).check(matches(allOf(withText("Fragment A"), isDisplayed())));

    }

    @Test
    public void fragmentRootViewIdIsDynamicallyReplaced() {
        Matcher<View> button = withId(R.id.button);

        // The ID of the root view of the inflated layout comes from <fragment> element.
        onView(withChild(button)).check(matches(withId(R.id.fragment_element)));
    }

}
