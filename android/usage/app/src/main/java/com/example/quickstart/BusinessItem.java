package com.example.quickstart;

public class BusinessItem {

    private String name;
    private String description;

    public BusinessItem(String name, String description) {
        this.name = name;
        this.description = description;
    }

    public String getName() {
        return name;
    }

    public String getDescription() {
        return description;
    }

}
