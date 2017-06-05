package learning.espresso;

import android.support.test.espresso.AmbiguousViewMatcherException;
import android.support.test.espresso.NoMatchingViewException;
import android.support.test.espresso.core.deps.guava.base.Predicate;
import android.support.test.espresso.core.deps.guava.collect.Iterables;
import android.support.test.espresso.core.deps.guava.collect.Iterators;
import android.support.test.espresso.util.TreeIterables;
import android.support.v7.widget.RecyclerView;
import android.view.View;

import org.hamcrest.Description;
import org.hamcrest.Matcher;
import org.hamcrest.TypeSafeMatcher;

import java.util.Iterator;

import javax.annotation.Nullable;

public class CustomViewMatchers {

    public static Matcher<View> withPositionInRecyclerView(final int position, final Matcher<View> recyclerViewMatcher) {
        return new TypeSafeMatcher<View>() {
            @Override
            protected boolean matchesSafely(View view) {
                RecyclerView recycler = (RecyclerView) findView(recyclerViewMatcher, view.getRootView());
                View itemView = recycler.findViewHolderForAdapterPosition(position).itemView;
                return view == itemView;
            }

            @Override
            public void describeTo(Description description) {
                description.appendText("is item at position ");
                description.appendValue(position);
                description.appendText(" in recycler view: ");
                recyclerViewMatcher.describeTo(description);
            }
        };
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
