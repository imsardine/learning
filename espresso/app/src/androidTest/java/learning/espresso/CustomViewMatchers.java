package learning.espresso;

import android.support.v7.widget.RecyclerView;
import android.view.View;
import android.view.ViewParent;

import org.hamcrest.Description;
import org.hamcrest.Matcher;
import org.hamcrest.TypeSafeMatcher;

public class CustomViewMatchers {

    public static Matcher<View> atPositionInRecyclerView(final int position, final Matcher<View> recyclerViewMatcher) {
        return new TypeSafeMatcher<View>() {
            @Override
            protected boolean matchesSafely(View view) {
                ViewParent parent = view.getParent();
                if ((parent instanceof RecyclerView) && recyclerViewMatcher.matches(parent)) {
                    View itemView = ((RecyclerView) parent).findViewHolderForAdapterPosition(position).itemView;
                    return view == itemView;
                } else {
                    return false;
                }
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

}
