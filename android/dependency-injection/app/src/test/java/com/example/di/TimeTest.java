package com.example.di;

import org.junit.Rule;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnit;
import org.mockito.junit.MockitoRule;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.TimeZone;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.when;

public class TimeTest {

    @Rule
    public MockitoRule mockito = MockitoJUnit.rule();

    @Mock
    private JavaUtil javaUtil;

    @Test
    public void now() {
        Time time = new Time(javaUtil);
        when(javaUtil.currentTimeMillis()).thenReturn(1483236184000L); // 2017-01-01 02:03:04 (GMT)

        Date now = time.now();
        assertEquals("2017-01-01 02:03:04", formatDateGmt(now));
    }

    @Test
    public void today() {
        Time time = new Time(javaUtil);
        when(javaUtil.currentTimeMillis()).thenReturn(1483228800000L); // 2017-01-01 02:03:04 (GMT)

        Date today = time.today();
        assertEquals("2017-01-01 00:00:00", formatDateGmt(today));
    }

    private String formatDateGmt(Date date) {
        SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        format.setTimeZone(TimeZone.getTimeZone("GMT"));
        return format.format(date);
    }

}
