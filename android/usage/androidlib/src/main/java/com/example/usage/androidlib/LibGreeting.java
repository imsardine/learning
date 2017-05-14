package com.example.usage.androidlib;

public class LibGreeting {

    public String hello(String somebody) {
        // who = (somebody == null || "".equals(somebody)) ? "World" : who;
        if (somebody == null || "".equals(somebody)) {
            somebody = "World";
        }

        return String.format("[AndroidLib] Hello, %1$s!", somebody);
    }

}
