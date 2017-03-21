package com.example.myapplication;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.annotation.Config;
import org.robolectric.Robolectric;
import org.robolectric.RobolectricTestRunner;

import android.app.Activity;
import android.widget.TextView;

import static org.junit.Assert.*;

@RunWith(RobolectricTestRunner.class)
@Config(constants = BuildConfig.class)
public class RobolectricTest {

    @Test
    public void test() {
        Activity activity = Robolectric.setupActivity(MainActivity.class);
        TextView greeting = (TextView) activity.findViewById(R.id.greeting);

        assertEquals("Hello World!", greeting.getText().toString());
    }

}

