package learning.espresso;

import android.support.test.espresso.NoMatchingViewException;
import android.support.test.espresso.ViewAssertion;
import android.support.test.espresso.assertion.ViewAssertions;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.RecyclerView.ViewHolder;
import android.view.View;

import org.hamcrest.Matcher;

import static learning.espresso.EspressoUtils.findView;

public class CustomViewAssertions {

    public static RecyclerViewItemAssertion itemAtPosition(int position) {
        return new RecyclerViewItemAssertion(position);
    }

    public static class RecyclerViewItemAssertion implements ViewAssertion {

        private int position;

        private Matcher<View> childViewMatcher;

        private ViewAssertion viewAssertion;

        private RecyclerViewItemAssertion(int position) {
            this.position = position;
        }

        public RecyclerViewItemAssertion onChildView(Matcher<View> childViewMatcher) {
            this.childViewMatcher = childViewMatcher;
            return this;
        }

        public ViewAssertion matches(Matcher<View> viewMatcher) {
            this.viewAssertion = ViewAssertions.matches(viewMatcher);
            return this;
        }

        @Override
        public void check(View view, NoMatchingViewException noViewFoundException) {
            ViewHolder viewHolder = ((RecyclerView) view).findViewHolderForAdapterPosition(position);
            View viewAtPosition = childViewMatcher == null ?
                    viewHolder.itemView : findView(childViewMatcher, viewHolder.itemView);

            viewAssertion.check(viewAtPosition, null);
        }
    }

}
