package com.example.di;

import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.TimeZone;

public class Time {

    private JavaUtil javaUtil;

    public Time(JavaUtil javaUtil) {
        this.javaUtil = javaUtil;
    }

    public Date now() {
        return new Date(javaUtil.currentTimeMillis());
    }

    public Date today() {
        Calendar calendar = new GregorianCalendar(TimeZone.getTimeZone("GMT"));
        calendar.setTimeInMillis(javaUtil.currentTimeMillis());

        calendar.set(Calendar.HOUR, 0);
        calendar.set(Calendar.MINUTE, 0);
        calendar.set(Calendar.SECOND, 0);
        calendar.set(Calendar.MILLISECOND, 0);

        return calendar.getTime();
    }

}
