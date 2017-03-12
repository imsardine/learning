package com.example.di;

import java.util.HashMap;
import java.util.Map;

public class Injection {

    private static Map<Class, Object> mocks = new HashMap<>();

    public static <T> void mock(Class<T> type, T mock) {
        mocks.put(type, mock);
    }

    public static Time provideTime() {
        return provide(Time.class);
    }

    private static <T> T provide(Class<T> type) {
        if (mocks.containsKey(type)) {
            return (T) mocks.get(type);
        } else {
            throw new RuntimeException("Dependency of type " + type.getName() + " cannot be served.");
        }
    }

}
