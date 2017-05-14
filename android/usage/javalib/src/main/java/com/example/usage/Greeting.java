package com.example.usage;

public class Greeting {

    public String hello(String somebody) {
        // who = (somebody == null || "".equals(somebody)) ? "World" : who;
        if (somebody == null || "".equals(somebody)) {
            somebody = "World";
        }

        return String.format("Hello, %1$s!", somebody);
    }

}
