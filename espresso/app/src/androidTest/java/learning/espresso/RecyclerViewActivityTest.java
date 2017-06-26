package learning.espresso;

import android.support.test.rule.ActivityTestRule;
import android.view.View;

import org.hamcrest.Matcher;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;

import static android.support.test.espresso.Espresso.onView;
import static android.support.test.espresso.action.ViewActions.click;
import static android.support.test.espresso.assertion.ViewAssertions.matches;
import static android.support.test.espresso.contrib.RecyclerViewActions.actionOnItemAtPosition;
import static android.support.test.espresso.contrib.RecyclerViewActions.scrollToPosition;
import static android.support.test.espresso.matcher.ViewMatchers.isChecked;
import static android.support.test.espresso.matcher.ViewMatchers.isDescendantOfA;
import static android.support.test.espresso.matcher.ViewMatchers.withId;
import static android.support.test.espresso.matcher.ViewMatchers.withText;
import static learning.espresso.CustomViewMatchers.atPositionInRecyclerView;
import static learning.espresso.RecyclerViewActionsExtension.itemAtPosition;
import static learning.espresso.RecyclerViewActionsExtension.onChildView;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.not;

@RunWith(JUnit4.class)
public class RecyclerViewActivityTest {

    @Rule
    public ActivityTestRule<RecyclerViewActivity> activityRule = new ActivityTestRule<>(RecyclerViewActivity.class);

    @Test
    public void clickItemOffScreen_atPositionInRecyclerView() {
        Matcher<View> itemAtPosition = atPositionInRecyclerView(29, withId(R.id.recycler));

        onView(withId(R.id.recycler)).perform(scrollToPosition(29));
        onView(allOf(withId(R.id.item_text), isDescendantOfA(itemAtPosition))).check(matches(withText("Item 30")));
        onView(allOf(withId(R.id.item_checkbox), isDescendantOfA(itemAtPosition))).perform(click());
        onView(withId(R.id.selected_item)).check(matches(withText("Item 30")));
    }

    @Test
    public void clickItemOffScreen_atPositionOnChildView() throws InterruptedException {
        onView(withId(R.id.recycler)).perform(scrollToPosition(30)).check(
                itemAtPosition(30).onChildView(withId(R.id.item_checkbox)).matches(not(isChecked())));

        onView(withId(R.id.recycler)).perform(actionOnItemAtPosition(1, onChildView(withId(R.id.item_checkbox), click())));

        onView(withId(R.id.recycler)).check(itemAtPosition(1).onChildView(withId(R.id.item_checkbox)).matches(isChecked()));
        onView(withId(R.id.selected_item)).check(matches(withText("Item 2")));
    }

}
