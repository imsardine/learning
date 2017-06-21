package learning.espresso;

import android.support.test.espresso.UiController;
import android.support.test.espresso.ViewAction;
import android.view.View;
import android.view.ViewGroup;

import org.hamcrest.Matcher;

import static android.support.test.espresso.matcher.ViewMatchers.isAssignableFrom;
import static android.support.test.espresso.matcher.ViewMatchers.isDisplayingAtLeast;
import static learning.espresso.EspressoUtils.findView;
import static org.hamcrest.Matchers.allOf;

public class CustomViewActions {

    public static ViewAction onChildView(Matcher<View> childViewMatcher, ViewAction viewAction) {
        return new ChildViewAction(childViewMatcher, viewAction);
    }

    private static class ChildViewAction implements ViewAction {

        private Matcher<View> childViewMatcher;

        private ViewAction viewAction;

        private ChildViewAction(Matcher<View> childViewMatcher, ViewAction viewAction) {
            this.childViewMatcher = childViewMatcher;
            this.viewAction = viewAction;
        }

        @Override
        public Matcher<View> getConstraints() {
            return allOf(isAssignableFrom(ViewGroup.class), isDisplayingAtLeast(90));
        }

        @Override
        public String getDescription() {
            return String.format("perform action: %s on child view matching: %s",
                    viewAction.getDescription(), childViewMatcher);
        }

        @Override
        public void perform(UiController uiController, View view) {
            View childView = findView(childViewMatcher, view);
            viewAction.perform(uiController, childView);
        }
    }

}
