package com.example.di;

import android.support.test.rule.ActivityTestRule;
import android.support.test.runner.AndroidJUnit4;
import android.widget.TextView;

import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnit;
import org.mockito.junit.MockitoRule;

import java.util.GregorianCalendar;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.when;

@RunWith(AndroidJUnit4.class)
public class MainActivityTest {

    @Rule
    public ActivityTestRule<MainActivity> activityRule = new ActivityTestRule<>(MainActivity.class, false, false);

    @Rule
    public MockitoRule mockito = MockitoJUnit.rule();

    @Mock
    private Time time;

    @Before
    public void setUp() {
        Injection.mock(Time.class, time);
        when(time.today()).thenReturn(new GregorianCalendar(2017, 0, 1).getTime());

        activityRule.launchActivity(null);
    }

    @Test
    public void initialState() {
        TextView greeting = (TextView) activityRule.getActivity().findViewById(R.id.greeting);
        assertEquals("Hello, World! (2017-01-01 00:00:00)", greeting.getText().toString());
    }

}
