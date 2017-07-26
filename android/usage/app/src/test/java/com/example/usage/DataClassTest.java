package com.example.usage;

import com.google.gson.Gson;

import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class DataClassTest {

    @Test
    public void touchNothing() {
    }

    @Test
    public void instantiateExplicitly() {
        DataClass data = new DataClass();
    }

    @Test
    public void instantiateViaReflection() throws Exception {
        DataClass data = DataClass.class.getConstructor(new Class[0]).newInstance(new Object[0]);
    }

    @Test
    public void instantiateViaGson() {
        Gson gson = new Gson();
        DataClass data = gson.fromJson("{\"name\": \"Jeremy\"}", DataClass.class);

        assertEquals("Jeremy", data.name);
    }

}
