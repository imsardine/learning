package myapp;

import java.io.PrintStream;
import java.io.ByteArrayOutputStream;
import java.text.SimpleDateFormat;
import java.text.ParseException;

import org.junit.Test;
import org.junit.Rule;
import org.junit.Before;
import static org.junit.Assert.*;

import org.mockito.Mock;
import org.mockito.junit.MockitoJUnit;
import org.mockito.junit.MockitoRule;
import static org.mockito.Mockito.*;

public class TestableGreetingTest {

    @Rule
    public MockitoRule mockito = MockitoJUnit.rule();

    private TestableGreeting greeting;

    private ByteArrayOutputStream out;

    @Mock
    private Timer timer;

    @Before
    public void setUp() {
        out = new ByteArrayOutputStream();
        this.greeting = new TestableGreeting(new PrintStream(out), timer); // test doubles
    }

    @Test
    public void greet_SunRise_GoodMorning() {
        when(timer.currentTimeMillis()).thenReturn(at("2017-10-25 06:10:00"));
        greeting.run();
        assertEquals("Good morning!\n", out.toString());
    }

    @Test
    public void greet_LaunchTime_GoodAfternoon() {
        when(timer.currentTimeMillis()).thenReturn(at("2017-10-25 12:10:00"));
        greeting.run();
        assertEquals("Good afternoon!\n", out.toString());
    }

    @Test
    public void greet_Sunset_GoodEvening() {
        when(timer.currentTimeMillis()).thenReturn(at("2017-10-25 18:00:00"));
        greeting.run();
        assertEquals("Good evening!\n", out.toString());
    }

    private long at(String time) {
        SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        try {
            return format.parse(time).getTime();
        } catch (ParseException e) {
            throw new RuntimeException(e);
        }
    }

}
