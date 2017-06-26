package learning.espresso;

import android.support.test.espresso.AmbiguousViewMatcherException;
import android.support.test.espresso.NoMatchingViewException;
import android.support.test.espresso.UiController;
import android.support.test.espresso.ViewAction;
import android.support.test.espresso.ViewAssertion;
import android.support.test.espresso.assertion.ViewAssertions;
import android.support.test.espresso.core.deps.guava.base.Predicate;
import android.support.test.espresso.core.deps.guava.collect.Iterables;
import android.support.test.espresso.core.deps.guava.collect.Iterators;
import android.support.test.espresso.util.TreeIterables;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.RecyclerView.ViewHolder;
import android.view.View;
import android.view.ViewGroup;

import org.hamcrest.Matcher;

import java.util.Iterator;

import javax.annotation.Nullable;

import static android.support.test.espresso.matcher.ViewMatchers.isAssignableFrom;
import static android.support.test.espresso.matcher.ViewMatchers.isDisplayingAtLeast;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.any;

public class RecyclerViewActionsExtension {

    public static ViewAction onChildView(Matcher<View> childMatcher, ViewAction viewAction) {
        return new ChildViewAction(childMatcher, viewAction);
    }

    public static RecyclerViewItemAssertion itemAtPosition(int position) {
        return new RecyclerViewItemAssertion(position);
    }

    private static class ChildViewAction implements ViewAction {

        private Matcher<View> childMatcher;

        private ViewAction viewAction;

        private ChildViewAction(Matcher<View> childMatcher, ViewAction viewAction) {
            this.childMatcher = childMatcher;
            this.viewAction = viewAction;
        }

        @Override
        public Matcher<View> getConstraints() {
            return allOf(isAssignableFrom(ViewGroup.class), isDisplayingAtLeast(90));
        }

        @Override
        public String getDescription() {
            return String.format("perform action: %s on child view matching: %s",
                    viewAction.getDescription(), childMatcher);
        }

        @Override
        public void perform(UiController uiController, View view) {
            View childView = findView(childMatcher, view);
            viewAction.perform(uiController, childView);
        }
    }

    public static class RecyclerViewItemAssertion implements ViewAssertion {

        private int position;

        private Matcher<View> childMatcher;

        private ViewAssertion viewAssertion = ViewAssertions.matches(any(View.class));

        private RecyclerViewItemAssertion(int position) {
            this.position = position;
        }

        public RecyclerViewItemAssertion onChildView(Matcher<View> childMatcher) {
            this.childMatcher = childMatcher;
            return this;
        }

        public ViewAssertion matches(Matcher<View> viewMatcher) {
            this.viewAssertion = ViewAssertions.matches(viewMatcher);
            return this;
        }

        public ViewAssertion doesNotExist() {
            this.viewAssertion = ViewAssertions.doesNotExist();
            return this;
        }

        @Override
        public void check(View view, NoMatchingViewException noViewFoundException) {
            ViewHolder viewHolder = ((RecyclerView) view).findViewHolderForAdapterPosition(position);

            try {
                View viewAtPosition = childMatcher == null ?
                        viewHolder.itemView : findView(childMatcher, viewHolder.itemView);
                viewAssertion.check(viewAtPosition, null);
            } catch (NoMatchingViewException e) {
                viewAssertion.check(null, e);
            }
        }
    }

    private static View findView(Matcher<View> matcher, View root) {
        Iterator<View> matches = matchedViewIterator(root, matcher);
        if (matches.hasNext()) {
            View match = matches.next();
            if (matches.hasNext()) {
                throw new AmbiguousViewMatcherException.Builder()
                        .withRootView(root)
                        .withViewMatcher(matcher)
                        .withView1(match)
                        .withView2(matches.next())
                        .withOtherAmbiguousViews(Iterators.toArray(matches, View.class))
                        .build();
            } else {
                return match;
            }

        } else {
            throw new NoMatchingViewException.Builder()
                    .withViewMatcher(matcher)
                    .withRootView(root)
                    .build();
        }
    }

    private static Iterator<View> matchedViewIterator(View root, final Matcher<View> matcher) {
        Predicate<View> predicate = new Predicate<View>() {
            @Override
            public boolean apply(@Nullable View view) {
                return view != null && matcher.matches(view);
            }
        };

        return Iterables.filter(TreeIterables.breadthFirstViewTraversal(root), predicate).iterator();
    }


}