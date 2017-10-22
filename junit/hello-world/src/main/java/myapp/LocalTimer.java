package myapp;

public class LocalTimer implements Timer {

    public long currentTimeMillis() {
        return System.currentTimeMillis();
    }

}
