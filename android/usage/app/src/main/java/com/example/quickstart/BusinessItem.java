package com.example.quickstart;

public class BusinessItem {

    private String id;
    private String name;
    private String description;

    public BusinessItem(String id, String name, String description) {
        this.id = id;
        this.name = name;
        this.description = description;
    }

    public String getID() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getDescription() {
        return description;
    }

}
