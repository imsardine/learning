package com.example.usage.androidlib;

import com.example.usage.Greeting;

public class LibGreeting {

    private Greeting delegate;

    public LibGreeting() {
        delegate = new Greeting();
    }

    public String hello(String somebody) {
        return "[AndroidLib] " + delegate.hello(somebody);
    }

}
