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
import static android.support.test.espresso.matcher.ViewMatchers.withId;
import static android.support.test.espresso.matcher.ViewMatchers.withParent;
import static android.support.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;

public class FragmentViaViewGroupActivityTest {

    @Rule
    public ActivityTestRule<FragmentViaViewGroupActivity> activityTestRule = new ActivityTestRule<>(FragmentViaViewGroupActivity.class);

    @Test
    public void fragmentIsDisplayed() {
        Matcher<View> button = withId(R.id.button);
        onView(button).check(matches(allOf(withText("Fragment A"), isDisplayed())));
    }

    @Test
    public void fragmentRootViewIdIsDynamicallyReplaced() {
        // Adding a fragment to an existing ViewGroup programmatically, the structure and IDs of
        // both container (fragment_placeholder) and root view of the fragment's layout (fragment_root)
        // are preserved.
        onView(withId(R.id.button)).check(matches(withParent(withId(R.id.fragment_root))));
        onView(withId(R.id.fragment_root)).check(matches(withParent(withId(R.id.fragment_placeholder))));
    }

}
