package io.github.imsardine.learning.jacoco;

public class Hello {

    public static void main(String[] args) {
        String whom = args.length > 0 ? args[0] : "World";
        System.out.println("Hello, " + whom + "!");
    }

} 
