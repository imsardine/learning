package com.example.di;

import android.content.Context;

public class Injection {

    private static Time time = new Time(new JavaUtil());

    public static Time provideTime() {
        return time;
    }

}
